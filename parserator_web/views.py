import usaddress

from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError


class Home(TemplateView):
    template_name = 'parserator_web/index.html'


class AddressParse(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        address = request.query_params.get('address', None)
        if not address:
            return Response({'error': "No address provided."}, status=400)
        
        try: 
            address_components, address_type = self.parse(address)

            return Response({
                'input_string': address,
                'address_components': address_components,
                'address_type': address_type
            })
        
        except ParseError as e:
            return Response({'error': str(e)}, status=400)

    def parse(self, address):
        try: 
            parsed_components, address_type = usaddress.tag(address)
            address_components = dict(parsed_components)
            return address_components, address_type
        
        except usaddress.RepeatedLabelError as e:
            raise ParseError(f"Repeated label error: {e}")
        
        except usaddress.RepeatedLabelWarning as e:
            raise ParseError(f"Repeated label warning: {e}")
        
        except Exception as e:
            raise ParseError(f"An unexpected error occurred: {str(e)}")
        
        
