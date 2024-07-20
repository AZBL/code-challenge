import pytest
from django.urls import reverse

def test_api_parse_succeeds(client):
    # TODO: Finish this test. Send a request to the API and confirm that the
    # data comes back in the appropriate format.
    address_string = '123 main st chicago il'
    
    response = client.get(reverse('address-parse'), {'address': address_string})

    assert response.status_code == 200
    data = response.json()
    assert 'input_string' in data
    assert 'address_components' in data
    assert 'address_type' in data

def test_api_parse_raises_error(client):
    # TODO: Finish this test. The address_string below will raise a
    # RepeatedLabelError, so ParseAddress.parse() will not be able to parse it.
    address_string = '123 main st chicago il 123 main st'
    
    response = client.get(reverse('address-parse'), {'address': address_string})

    assert response.status_code == 400
    data = response.json()
    assert 'error' in data
    assert data['error'].startswith('Repeated label error:') or 'ERROR: Unable to tag this string because more than one area of the string has the same label' in data['error']
