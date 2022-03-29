import connexion
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_covid_symptom_annotation_request import TextCovidSymptomAnnotationRequest  # noqa: E501
from openapi_server.models.text_covid_symptom_annotation_response import TextCovidSymptomAnnotationResponse  # noqa: E501
from openapi_server.models.text_covid_symptom_annotation import TextCovidSymptomAnnotation  # noqa: E501
import re

import re
patterns = dict()
condition_dict = {'abdominal pain':'abdominal_pain','chest pain':'chest_pain','chill':'chill','cough':'cough','cyanosis':'cyanosis','delirium':'delirium','diarrhea':'diarrhea','dyspnea':'dyspnea','fatigue':'fatigue','fever':'fever','headache':'headache','hypersomnia':'hypersomnia','loss of appetite':'loss_of_appetite','loss of smell':'loss_of_smell','loss of taste':'loss_of_taste','myalgia':'myalgia','nasal obstruction':'nasal_obstruction','nausea':'nausea','sore throat':'sore_throat','vomiting':'vomiting', 'shortness of breath':'nasal_obstruction', 'muscle ache':"chill"}
for i in condition_dict.keys():
    patterns[condition_dict[i]] = re.compile(i,re.IGNORECASE)


def create_text_covid_symptom_annotations(text_covid_symptom_annotation_request=None):  # noqa: E501
    """Annotate COVID symptoms in a clinical note

    Return the COVID symptom annotations found in a clinical note # noqa: E501

    :param text_covid_symptom_annotation_request:
    :type text_covid_symptom_annotation_request: dict | bytes

    :rtype: TextCovidSymptomAnnotationResponse
    """
    res = None
    status = None
    if connexion.request.is_json:
        try:
            annotation_request = TextCovidSymptomAnnotationRequest.from_dict(
                connexion.request.get_json())  # noqa: E501
            note = annotation_request._note
            annotations = []

            for ptn_name in patterns:
                pattern = patterns[ptn_name]
                matches = pattern.finditer(note._text)
                add_covid_symptom_annotation(annotations, matches, ptn_name)

            res = TextCovidSymptomAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            res = Error("Internal error", status, str(error))

    return res, status


def add_covid_symptom_annotation(annotations, matches, condition):
    """
    Converts matches to TextCovidSymptomAnnotation objects and adds them to the
    annotations array specified.
    """
    for match in matches:
        annotations.append(TextCovidSymptomAnnotation(
            start=match.start(),
            length=len(match[0]),
            text=match[0],
            condition=condition,
            certainty="positive",
            confidence=95.5
        ))
