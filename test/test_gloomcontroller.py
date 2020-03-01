import logging
import unittest
import sys
from unittest import mock
import random
sys.path.insert(0, '../')
sys.path.insert(0, './')
from gloomcontroller import Controller  # noqa

logging.basicConfig(level=logging.WARN, format='')


class TestGloomlogController(unittest.TestCase):
    """
    Test GloomLog's Controller class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up variables for testing
        """

        logging.info(
            "Setting up variables for testing GloomLog's Controller class")

        cls.controller = Controller()

    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("gloomview.UserInterfaceMain.present_interface")
    def test_run_once(self, mock_present, mock_exit):
        """
        Test whether run can correctly exit a loop
        """

        logging.info(
            "Testing whether run can correctly exit a loop"
        )

        mock_present.return_value = False

        self.controller.run()

        mock_exit.assert_called_once()

    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("gloomview.UserInterfaceMain.present_interface")
    def test_run_loops(self, mock_present, mock_exit):
        """
        Test whether run can correctly exit a loop after a couple of iterations
        """

        logging.info(
            "Testing whether run can correctly exit a loop after a couple of iterations"
        )

        mock_list = [True for _ in range(random.randint(4, 50))]
        mock_list.append(False)
        mock_present.side_effect = mock_list

        self.controller.run()

        self.assertEqual(len(mock_present.mock_calls), len(mock_list))
        mock_exit.assert_called_once()

    @mock.patch("gloomcontroller.Backend.check_saves")
    @mock.patch("gloomcontroller.Backend.save_to_file")
    @mock.patch("gloomcontroller.UserInterfaceMain.prepare_save_interface")
    @mock.patch("gloomcontroller.Backend.load_save_file_as_text")
    @mock.patch("gloomcontroller.Controller.exit_gloomlog")
    @mock.patch("gloomview.UserInterfaceMain.present_interface")
    def test_run_complex(
        self,
        mock_present,
        mock_exit,
        mock_load,
        mock_prepare,
        mock_save,
        mock_checksaves
    ):
        """
        Test whether controller can correctly parse return values
        """

        logging.info(
            "Testing whether controller can correctly parse return values"
        )

        mock_list = [True for _ in range(random.randint(4, 50))]
        mock_list.append(("abc", "def"))
        mock_list.append("xyz")
        random.shuffle(mock_list)
        mock_list.append(False)
        mock_present.side_effect = mock_list

        mock_load.return_value = "zyx"
        mock_checksaves.return_value = ["k", "l.k", "mlk"]

        self.controller.run()

        self.assertEqual(len(mock_present.mock_calls), len(mock_list))
        mock_load.assert_called_once_with(save_file="xyz")
        mock_prepare.assert_called_once_with(
            save_file="xyz",
            save_text="zyx"
        )
        mock_save.assert_called_once_with(save_file="abc", save_info="def")
        self.assertEqual(
            self.controller.interface.list_saves,
            ["k", "l.k", "mlk"]
        )
        mock_exit.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
