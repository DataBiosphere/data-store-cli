import errno
import os
import shutil
import sys
import tempfile
import threading
import unittest

import scandir
import six
from mock import patch

from hca.dss import DSSClient


def _touch_file(path):
    try:
        os.makedirs(os.path.split(path)[0])
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    with open(path, 'w'):
        pass


def _fake_download_file(*args, **kwargs):
    _touch_file(args[2])


class TestManifestDownload(unittest.TestCase):
    manifest = list(zip(
        ('bundle_uuid', 'a_uuid', 'b_uuid', 'c_uuid'),
        ('bundle_version', '1_version', '1_version', '1_version'),
        ('file_content_type', 'somestuff', 'somestuff', 'somestuff'),
        ('file_name', 'a_file_name', 'b_file_name', 'c_file_name'),
        ('file_sha256',
         'ad3fc1e4898e0bce096be5151964a81929dbd2a92bd5ed56a39a8e133053831d',
         '8F35071EAEEDD9D6F575A8B0F291DAEAC4C1DFDFA133B5C561232A00BF18C4B4',
         '8f3404db04bdede03e9128a4b48599d0ecde5b2e58ed9ce52ce84c3d54a3429c'),
        ('file_size', '12', '2', '41'),
        ('file_uuid', 'af_uuid', 'bf_uuid', 'cf_uuid'),
        ('file_version', 'af_version', 'af_version', 'af_version'),
        ('file_indexed', 'False', 'False', 'False'),
    ))
    version_dir = os.path.join('.', '.hca', 'v2', 'files_2_4')

    def setUp(self):
        self.prev_wd = os.getcwd()
        self.tmp_dir = tempfile.mkdtemp()
        os.chdir(self.tmp_dir)
        self.dss = DSSClient()
        self._write_manifest(self.manifest)
        self.manifest_file = 'manifest.tsv'

    def tearDown(self):
        os.chdir(self.prev_wd)
        shutil.rmtree(self.tmp_dir)

    def _write_manifest(self, manifest):
        with open('manifest.tsv', 'w') as f:
            f.write('\n'.join(['\t'.join(row) for row in manifest]))

    def _assert_all_files_downloaded(self):
        files_present = {os.path.join(dir_path, f)
                         for dir_path, _, files in scandir.walk('.')
                         for f in files}
        files_expected = {
            os.path.join('.', os.path.basename(self.manifest_file)),
            os.path.join(self.version_dir, 'ad', '3fc1', 'ad3fc1e4898e0bce096be5151964a81929dbd2a92bd5ed56a39a8e133053831d'),
            os.path.join(self.version_dir, '8f', '3507', '8f35071eaeedd9d6f575a8b0f291daeac4c1dfdfa133b5c561232a00bf18c4b4'),
            os.path.join(self.version_dir, '8f', '3404', '8f3404db04bdede03e9128a4b48599d0ecde5b2e58ed9ce52ce84c3d54a3429c'),
        }
        self.assertEqual(files_present, files_expected)

    def _assert_manifest_updated_with_paths(self):
        output_manifest = os.path.basename(self.manifest_file)
        self.assertTrue(os.path.isfile(output_manifest))
        with open(output_manifest, 'r') as f:
            output_manifest = [tuple(line.split('\t')) for line in f.read().splitlines()]
        expected_manifest = list(zip(*self.manifest))
        version_dir = os.path.join('.hca', 'v2', 'files_2_4')
        expected_manifest.append((
            'file_path',
            os.path.join(version_dir, 'ad', '3fc1', 'ad3fc1e4898e0bce096be5151964a81929dbd2a92bd5ed56a39a8e133053831d'),
            os.path.join(version_dir, '8f', '3507', '8f35071eaeedd9d6f575a8b0f291daeac4c1dfdfa133b5c561232a00bf18c4b4'),
            os.path.join(version_dir, '8f', '3404', '8f3404db04bdede03e9128a4b48599d0ecde5b2e58ed9ce52ce84c3d54a3429c')
        ))
        expected_manifest = list(zip(*expected_manifest))
        self.assertEqual(output_manifest, expected_manifest)

    def _assert_manifest_not_updated(self):
        for row in self.dss._parse_manifest(self.manifest_file):
            self.assertNotIn('file_path', row)

    @patch('hca.dss.DSSClient.DIRECTORY_NAME_LENGTHS', [1, 3, 2])
    def test_file_path(self):
        self.assertRaises(AssertionError, self.dss._file_path, 'a')
        parts = self.dss._file_path('abcdefghij').split(os.sep)
        self.assertEqual(parts, ['.hca', 'v2', 'files_1_3_2', 'a', 'bcd', 'ef', 'abcdefghij'])

    @patch('logging.Logger.warning')
    @patch('hca.dss.DSSClient._download_file', side_effect=_fake_download_file)
    def test_manifest_download(self, download_func, warning_log):
        self.dss.download_manifest_v2(self.manifest_file, 'aws')
        self.assertEqual(download_func.call_count, len(self.manifest) - 1)
        self.assertEqual(warning_log.call_count, 1, 'Only expected warning for overwriting manifest')
        # Since files now exist, running again ensures that we avoid unnecessary downloads
        self.dss.download_manifest_v2(self.manifest_file, 'aws')
        self.assertEqual(warning_log.call_count, 2, 'Only expected warning for overwriting manifest')
        self.assertEqual(download_func.call_count, len(self.manifest) - 1)
        self._assert_all_files_downloaded()
        self._assert_manifest_updated_with_paths()

    @patch('logging.Logger.warning')
    @patch('hca.dss.DSSClient._download_file', side_effect=_fake_download_file)
    def test_manifest_download_different_path(self, download_func, warning_log):
        # Move manifest file so it is not overwritten on download
        os.mkdir('my_manifest_dir')
        new_manifest_path = os.path.join('my_manifest_dir', self.manifest_file)
        os.rename(self.manifest_file, new_manifest_path)
        self.manifest_file = new_manifest_path
        self.dss.download_manifest_v2(self.manifest_file, 'aws')
        self.assertEqual(download_func.call_count, len(self.manifest) - 1)
        self.assertEqual(warning_log.call_count, 0)
        # Since files now exist, running again ensures that we avoid unnecessary downloads
        self.dss.download_manifest_v2(self.manifest_file, 'aws')
        self.assertEqual(warning_log.call_count, 1, 'Only expected warning for overwriting manifest')
        self.assertEqual(download_func.call_count, len(self.manifest) - 1)
        # Remove the original manifest file for accurate count
        os.remove(new_manifest_path)
        self._assert_all_files_downloaded()
        self._assert_manifest_updated_with_paths()

    @patch('logging.Logger.warning')
    @patch('hca.dss.DSSClient._download_file', side_effect=_fake_download_file)
    def test_manifest_download_partial(self, _, warning_log):
        """Test download when some files are already present"""
        _touch_file(self.dss._file_path(self.manifest[1][4]))
        self.dss.download_manifest_v2(self.manifest_file, 'aws')
        self.assertEqual(warning_log.call_count, 1, 'Only expected warning for overwriting manifest')
        self._assert_all_files_downloaded()
        self._assert_manifest_updated_with_paths()

    @patch('logging.Logger.warning')
    @patch('hca.dss.DSSClient._download_file', side_effect=[None, ValueError(), KeyError()])
    def test_manifest_download_failed(self, _, warning_log):
        self.assertRaises(RuntimeError, self.dss.download_manifest_v2, self.manifest_file, 'aws')
        self.assertEqual(warning_log.call_count, 2)
        self._assert_manifest_not_updated()

    @unittest.skipIf(sys.version_info < (3,), 'Threading.Barrier is not available in Python 2')
    def test_manifest_download_parallel(self):
        """
        The goal is to make sure the download of the file happens simultaneously in multiple threads.

        The approach is to mock the old download_file function with a replacement that runs the same code but waits
        for at least two threads to be ready before beginning.
        """
        # make a new manifest with all the same hashes
        new_manifest = [self.manifest[0]]
        for row in self.manifest[1:]:
            new_row = list(row)
            new_row[4] = 'fakeHASH'
            new_manifest.append(new_row)
        self._write_manifest(new_manifest)
        barrier = threading.Barrier(3)

        def _fake_do_download_file_with_barrier(*args, **kwargs):
            """
            Wait for friends before trying to "download" the same fake file
            """
            barrier.wait()
            fh = args[3]
            fh.write(six.b('Here we write some stuff so that the fake download takes some time. '
                           'This helps ensure that multiple threads are writing at once and thus '
                           'allows us to test for race conditions.'))
            return 'FAKEhash'

        with patch('hca.dss.DSSClient._do_download_file', side_effect=_fake_do_download_file_with_barrier):
            self.dss.download_manifest_v2('manifest.tsv', 'aws', threads=3)
        files_present = {os.path.join(dir_path, f)
                         for dir_path, _, files in scandir.walk('.')
                         for f in files}
        files_expected = {
            os.path.join('.', 'manifest.tsv'),
            os.path.join(self.version_dir, 'fa', 'keha', 'fakehash')
        }
        self.assertEqual(files_present, files_expected)


if __name__ == "__main__":
    unittest.main()