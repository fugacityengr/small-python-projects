import bagels
import unittest
from unittest.mock import patch


def generate_array(n, value):
    """
    Helper function to generate arrays of length n filled with value
    """
    return [value for n in range(n)]


# Mock print to capture the print output
# Mock input to simulate user input
# Mock secretnum to have control on the number to guess
@patch("builtins.print")
@patch("builtins.input")
@patch("bagels.getSecretNum", return_value="123", create=True)
class TestBagelsGameLogic(unittest.TestCase):
    """Test game logic if working correctly"""

    def test_bagels_correct_answer_first_try(
        self, mockSecretNumber, mockInput, mockPrint
    ):
        mockInput.return_value = f"{bagels.getSecretNum.return_value}"
        bagels.main()
        # Only tests the last print statement which is Thanks for playing
        mockPrint.assert_called_with("Thanks for playing!")

        # Test if the correct sequence of statements was printed
        assert "call('Guess #1')" in str(mockPrint.call_args_list)
        assert not "call('Guess #10')" in str(mockPrint.call_args_list)
        assert "call('You got it!')" == str((mockPrint.call_args_list)[-3])
        assert "call('Do you want to play again? (yes or no)')" == str(
            (mockPrint.call_args_list)[-2]
        )
        assert "call('Thanks for playing!')" == str((mockPrint.call_args_list)[-1])

        # # Reveal what was printed
        # import sys

        # # # Reveal what was last printed
        # # # sys.stdout.write(str(mockPrint.call_args) + "\n")
        # # # Reveal all the calls to print
        # sys.stdout.write(str(mockPrint.call_args_list) + "\n")
        # sys.stdout.write(str(list(mockPrint.call_args_list)[-1]))

    def test_bagels_correct_answer_after_N_tries(
        self, mockSecretNumber, mockInput, mockPrint
    ):
        # Side effect can be used to simulate consecutive inputs
        # The test will fail if it cannot get outside the loop. Thus the extra (double) input after the correct answer.
        # mockInput.side_effect = ["111", "111", "123", "123"]
        # While this test case technically tests all N tries (including first try correct)
        # the first test case is still included to demonstrate difference between `.return_value` and `.side_effect`
        for num_attempts in range(10):
            user_inputs = generate_array(
                num_attempts,
                f"{bagels.getSecretNum.return_value[::-1]}",  # Make sure that the guess is incorrect by reversing the correct answer
            )
            # user_inputs.extend(["123", "123"])
            user_inputs.extend([f"{bagels.getSecretNum.return_value}"] * 2)
            mockInput.side_effect = user_inputs
            bagels.main()
            # The last "Guess #" to be printed must be the number of incorrect attempts + 1
            assert f"call('Guess #{num_attempts + 1}')" == str(
                (mockPrint.call_args_list)[-4]
            )
            assert "call('You got it!')" == str((mockPrint.call_args_list)[-3])
            assert "call('Do you want to play again? (yes or no)')" == str(
                (mockPrint.call_args_list)[-2]
            )
            assert "call('Thanks for playing!')" == str((mockPrint.call_args_list)[-1])
            # import sys

            # sys.stdout.write(f"INPUT call('Guess #{num_attempts + 1}')")
            # sys.stdout.write(f"OUTPUT {str((mockPrint.call_args_list)[-4])}")

    def test_bagels_no_correct_answer(self, mockSecretNumber, mockInput, mockPrint):
        mockInput.return_value = "456"
        bagels.main()
        assert "call('Guess #10')" == str((mockPrint.call_args_list)[-6])
        assert "call('Bagels')" == str((mockPrint.call_args_list)[-5])
        assert "call('You ran out of guesses.')" == str((mockPrint.call_args_list)[-4])
        assert f"call('The answer was {bagels.getSecretNum.return_value}')" == str(
            (mockPrint.call_args_list)[-3]
        )
        assert "call('Do you want to play again? (yes or no)')" == str(
            (mockPrint.call_args_list)[-2]
        )
        assert "call('Thanks for playing!')" == str((mockPrint.call_args_list)[-1])

        # import sys

        # sys.stdout.write(str(mockPrint.call_args_list) + "\n")

    def test_bagels_replay_after_correct_answer(
        self, mockSecretNumber, mockInput, mockPrint
    ):
        for num_attempts in range(10):
            user_inputs = generate_array(
                num_attempts,
                f"{bagels.getSecretNum.return_value[::-1]}",
            )
            user_inputs.extend(
                [
                    f"{bagels.getSecretNum.return_value}",
                    "yes",
                    f"{bagels.getSecretNum.return_value}",
                    "no",
                ]
            )
            mockInput.side_effect = user_inputs
            bagels.main()
            assert f"call('Guess #{num_attempts + 1}')" == str(
                (mockPrint.call_args_list)[-9]
            )
            assert "call('You got it!')" == str((mockPrint.call_args_list)[-8])
            assert "call('Do you want to play again? (yes or no)')" == str(
                (mockPrint.call_args_list)[-7]
            )
            assert "call('I have thought up a number.')" == str(
                (mockPrint.call_args_list)[-6]
            )
            assert "call('You have 10 guesses to get it.')" == str(
                (mockPrint.call_args_list)[-5]
            )
            assert "call('Guess #1')" == str((mockPrint.call_args_list)[-4])
            assert "call('You got it!')" == str((mockPrint.call_args_list)[-3])
            assert "call('Do you want to play again? (yes or no)')" == str(
                (mockPrint.call_args_list)[-2]
            )
            assert "call('Thanks for playing!')" == str((mockPrint.call_args_list)[-1])

        # import sys

        # sys.stdout.write(str(mockPrint.call_args_list) + "\n")

    def test_bagels_hint_fermi(self, mockSecretNumber, mockInput, mockPrint):
        mockInput.return_value = "145"
        bagels.main()

        assert "call('Fermi')" == str((mockPrint.call_args_list)[-5])

    def test_bagels_hint_pico(self, mockSecretNumber, mockInput, mockPrint):
        mockInput.return_value = "451"
        bagels.main()

        assert "call('Pico')" == str((mockPrint.call_args_list)[-5])

    def test_bagels_hint_bagels(self, mockSecretNumber, mockInput, mockPrint):
        mockInput.return_value = "456"
        bagels.main()

        assert "call('Bagels')" == str((mockPrint.call_args_list)[-5])

    def test_bagels_hint_alphabetization(self, mockSecretNumber, mockInput, mockPrint):
        mockInput.return_value = f"{bagels.getSecretNum.return_value[::-1]}"
        bagels.main()

        assert "call('Fermi Pico Pico')" == str((mockPrint.call_args_list)[-5])


if __name__ == "__main__":
    unittest.main()
