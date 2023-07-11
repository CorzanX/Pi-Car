
import os

from speech_model import ModelSpeech
from model_zoo.speech_model.keras_backend import SpeechModel251BN
from speech_features import Spectrogram
from language_model3 import ModelLanguage
def predict_speech_file(filename):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    AUDIO_LENGTH = 1600
    AUDIO_FEATURE_LENGTH = 200
    CHANNELS = 1
    # 默认输出的拼音的表示大小是1428，即1427个拼音+1个空白块
    OUTPUT_SIZE = 1428
    sm251bn = SpeechModel251BN(
        input_shape=(AUDIO_LENGTH, AUDIO_FEATURE_LENGTH, CHANNELS),
        output_size=OUTPUT_SIZE
    )
    feat = Spectrogram()
    ms = ModelSpeech(sm251bn, feat, max_label_length=64)

    # 声学模型识别
    ms.load_model('save_models/' + sm251bn.get_model_name() + '.model.h5')
    res = ms.recognize_speech_from_file(filename)

    ml = ModelLanguage('model_language')
    ml.load_model()
    str_pinyin = res
    res = ml.pinyin_to_text(str_pinyin)
    print('语音识别最终结果：\n', res)
    return res