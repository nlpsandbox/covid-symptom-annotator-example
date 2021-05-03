import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_covid_symptom_annotation_request import TextCovidSymptomAnnotationRequest  # noqa: E501
from openapi_server.models.text_covid_symptom_annotation_response import TextCovidSymptomAnnotationResponse  # noqa: E501
from openapi_server import util


def create_text_covid_symptom_annotations(text_covid_symptom_annotation_request=None):  # noqa: E501
    """Annotate COVID symptoms in a clinical note

    Return the COVID symptom annotations found in a clinical note # noqa: E501

    :param text_covid_symptom_annotation_request:
    :type text_covid_symptom_annotation_request: dict | bytes

    :rtype: TextCovidSymptomAnnotationResponse
    """
    if connexion.request.is_json:
        annotation_request = TextCovidSymptomAnnotationRequest.from_dict(connexion.request.get_json())  # noqa: E501

        note = annotation_request._note

    return 'do some magic!'
