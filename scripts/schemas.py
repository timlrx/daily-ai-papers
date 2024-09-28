from enum import Enum
from typing_extensions import TypedDict


class ClassificationChoices(Enum):
    """
    Taken from HF taxonomy
    """

    MULTIMODAL = "Multimodal"
    IMAGE_TEXT_TO_TEXT = "Image-Text-to-Text"
    VISUAL_QUESTION_ANSWERING = "Visual Question Answering"
    DOCUMENT_QUESTION_ANSWERING = "Document Question Answering"
    VIDEO_TEXT_TO_TEXT = "Video-Text-to-Text"
    ANY_TO_ANY = "Any-to-Any"
    COMPUTER_VISION = "Computer Vision"
    DEPTH_ESTIMATION = "Depth Estimation"
    IMAGE_CLASSIFICATION = "Image Classification"
    OBJECT_DETECTION = "Object Detection"
    IMAGE_SEGMENTATION = "Image Segmentation"
    TEXT_TO_IMAGE = "Text-to-Image"
    IMAGE_TO_TEXT = "Image-to-Text"
    IMAGE_TO_IMAGE = "Image-to-Image"
    IMAGE_TO_VIDEO = "Image-to-Video"
    UNCONDITIONAL_IMAGE_GENERATION = "Unconditional Image Generation"
    VIDEO_CLASSIFICATION = "Video Classification"
    TEXT_TO_VIDEO = "Text-to-Video"
    ZERO_SHOT_IMAGE_CLASSIFICATION = "Zero-Shot Image Classification"
    MASK_GENERATION = "Mask Generation"
    ZERO_SHOT_OBJECT_DETECTION = "Zero-Shot Object Detection"
    TEXT_TO_3D = "Text-to-3D"
    IMAGE_TO_3D = "Image-to-3D"
    IMAGE_FEATURE_EXTRACTION = "Image Feature Extraction"
    KEYPOINT_DETECTION = "Keypoint Detection"
    NATURAL_LANGUAGE_PROCESSING = "Natural Language Processing"
    TEXT_CLASSIFICATION = "Text Classification"
    TOKEN_CLASSIFICATION = "Token Classification"
    TABLE_QUESTION_ANSWERING = "Table Question Answering"
    QUESTION_ANSWERING = "Question Answering"
    ZERO_SHOT_CLASSIFICATION = "Zero-Shot Classification"
    TRANSLATION = "Translation"
    SUMMARIZATION = "Summarization"
    FEATURE_EXTRACTION = "Feature Extraction"
    TEXT_GENERATION = "Text Generation"
    TEXT2TEXT_GENERATION = "Text2Text Generation"
    FILL_MASK = "Fill-Mask"
    SENTENCE_SIMILARITY = "Sentence Similarity"
    AUDIO = "Audio"
    TEXT_TO_SPEECH = "Text-to-Speech"
    TEXT_TO_AUDIO = "Text-to-Audio"
    AUTOMATIC_SPEECH_RECOGNITION = "Automatic Speech Recognition"
    AUDIO_TO_AUDIO = "Audio-to-Audio"
    AUDIO_CLASSIFICATION = "Audio Classification"
    VOICE_ACTIVITY_DETECTION = "Voice Activity Detection"
    TABULAR = "Tabular"
    TABULAR_CLASSIFICATION = "Tabular Classification"
    TABULAR_REGRESSION = "Tabular Regression"
    TIME_SERIES_FORECASTING = "Time Series Forecasting"
    REINFORCEMENT_LEARNING = "Reinforcement Learning"
    ROBOTICS = "Robotics"
    OTHER = "Other"
    GRAPH_MACHINE_LEARNING = "Graph Machine Learning"


class PaperResponse(TypedDict):
    summary: str
    classification: list[ClassificationChoices]
    huggingface_urls: list[str]
    github_urls: list[str]
