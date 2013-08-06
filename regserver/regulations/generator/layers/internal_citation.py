from urlparse import urljoin
from django.template import loader, Context
from django.core.urlresolvers import reverse, NoReverseMatch
from ..node_types import to_markup_id

class InternalCitationLayer():
    def __init__(self, layer):
        self.layer = layer
        self.generate_sectional = False
        self.reg_version = None

    @staticmethod
    def render_url(citation_url, text, template_name):
        citation = {'url': citation_url, 
                    'label':text}
        c = Context({'citation':citation})
        template =  loader.get_template(template_name)
        return template.render(c).strip('\n')

    @staticmethod
    def create_sectional_url_parts(layer_element):
        citation_anchor = "#" + "-".join(to_markup_id(layer_element['citation']))
        section_url = '-'.join(layer_element['citation'][0:2])
        return (section_url, citation_anchor)

    @staticmethod
    def create_sectional_link(text, layer_element, reg_version, template_name='layers/internal_citation.html'):
        section_url, citation_anchor = InternalCitationLayer.create_sectional_url_parts(layer_element)
        try:
            citation_url = reverse('chrome_section_view', 
                kwargs={'label_id':section_url, 'version':reg_version})
            citation_url = citation_url + citation_anchor
        except NoReverseMatch:
            #XXX We have some errors in our layers. Once those are fixed, we need to 
            #revisit this. 
            citation_url = ''
        return InternalCitationLayer.render_url(citation_url, text, template_name)

    @staticmethod
    def create_link(text, layer_element, template_name='layers/internal_citation.html'):
        citation_url = "#" + "-".join(to_markup_id(layer_element['citation']))
        return InternalCitationLayer.render_url(citation_url, text, template_name)

    def apply_layer(self, text, text_index):    
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            layer_pairs = []
            for layer_element in layer_elements:
                for start, end in layer_element['offsets']:
                    ot = text[int(start):int(end)]

                    if self.generate_sectional:
                        rt = InternalCitationLayer.create_sectional_link(ot, layer_element, self.reg_version)
                    else:
                        rt = InternalCitationLayer.create_link(ot, layer_element)
                    layer_pairs.append((ot, rt, (start, end)))
            return layer_pairs
