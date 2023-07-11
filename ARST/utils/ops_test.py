

import pytest
from ops import get_edit_distance, ctc_decode_delete_tail_blank, ctc_decode_stream


class TestGetEditDistance:
    def test_1(self):
        examle_input = ["abc", "abc"]
        examle_output = 0
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output

    def test_2(self):
        examle_input = ["abc", "adc"]
        examle_output = 1
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output

    def test_3(self):
        examle_input = ["abc", "a"]
        examle_output = 2
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output

    def test_4(self):
        examle_input = ["abc", "addce"]
        examle_output = 3
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output

    def test_5(self):
        examle_input = ["abc", ""]
        examle_output = 3
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output

    def test_6(self):
        examle_input = ["", ""]
        examle_output = 0
        result = get_edit_distance(examle_input[0], examle_input[1])
        assert result == examle_output


class TestCtcDecodeDeleteTailBlank:
    def test_1(self):
        examle_input = [1, 2, 3, 4, 5, -1, -1, -1, -1, -1, -1]
        examle_output = [1, 2, 3, 4, 5]
        result = ctc_decode_delete_tail_blank(examle_input)
        assert result == examle_output

    def test_2(self):
        examle_input = [1, 2, 3, 4, 5, -1]
        examle_output = [1, 2, 3, 4, 5]
        result = ctc_decode_delete_tail_blank(examle_input)
        assert result == examle_output

    def test_3(self):
        examle_input = [1, 2, 3, 4, 5]
        examle_output = [1, 2, 3, 4, 5]
        result = ctc_decode_delete_tail_blank(examle_input)
        assert result == examle_output

    def test_4(self):
        examle_input = [-1, -1, -1, -1]
        examle_output = []
        result = ctc_decode_delete_tail_blank(examle_input)
        assert result == examle_output

    def test_5(self):
        examle_input = [-1]
        examle_output = []
        result = ctc_decode_delete_tail_blank(examle_input)
        assert result == examle_output


class TestCtcDecodeStream:
    def test_1(self):
        examle_input = [-1, -1, -1, 1, 1, 1, -1, -1, 2, 2, 2, 3, 3, -1, -1, -1]
        examle_output = [1, 2, 3, -1]
        result = []
        res, tmp = ctc_decode_stream(examle_input)
        result.append(res)
        while len(tmp) > 0:
            res, tmp = ctc_decode_stream(tmp)
            result.append(res)
        assert result == examle_output

    def test_2(self):
        examle_input = [-1, -1, -1, -1, -1]
        examle_output = [-1]
        result = []
        res, tmp = ctc_decode_stream(examle_input)
        result.append(res)
        while len(tmp) > 0:
            res, tmp = ctc_decode_stream(tmp)
            result.append(res)
        assert result == examle_output
