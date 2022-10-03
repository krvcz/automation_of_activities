from unittest.mock import patch, call
from automat import Automat
import pytest


@patch('pynput.mouse.Listener.start')
@patch('pynput.keyboard.Listener.start')
@patch('pynput.mouse.Listener.join')
@patch('pynput.keyboard.Listener.join')
def test_record_process(mock1, mock2, mock3, mock4):
    automat = Automat(delay = 0.0000001)
    automat.record_process()
    mock3.assert_called()
    mock4.assert_called()
    mock2.assert_called()
    mock1.assert_called()




@patch('automat.Automat.press_keyboard_button')
@patch('automat.Automat._parse_command_file', return_value=[{
        "eventType": "press_keyboard_button",
        "payload": {
            "button": "e"
        }
    },
    {
        "eventType": "press_keyboard_button",
        "payload": {
            "button": "backspace"
        }
    }])
def test_run_process(mock1, mock2):
    automat = Automat(delay = 0.0000001)
    with pytest.raises(Exception, match= 'Missing JSON file. \n Upload JSON file or record macro'):
        automat.run_process()

    command_list = 'file.json'

    automat.run_process(command_list)
    mock1.assert_called()
    calls = [call(button = 'e'), call(button = 'backspace')]
    mock2.assert_has_calls(calls)

