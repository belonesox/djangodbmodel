'''
 Generating graphical representation of application data model
'''

# from django.contrib.contenttypes.models import ContentType
from django.contrib.admindocs import utils
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.apps import apps


from django.conf import settings

from django.db.models.fields import related
from django.template.loader import get_template
from django.template import Context
import json

#pylint: disable=E1101, C0330 
#pylint: disable=W0212, W0612

import inspect
import ast

class ASTClassFilter(ast.NodeVisitor):
    def __init__(self):
        self.names = []

    def visit_Attribute(self, node):
        self.stats["name"].append(node.attr)
        self.generic_visit(node)


def dbmodel(request):
    '''
    Generate database model visualization for specified applications
    '''
    def get_id4model(app_label, model):
        '''
         Get id and url for a model
        '''
        url = "../models/" + app_label + "." + model + "/"
        return url
    
    graph_settings = getattr(settings, 'DBMODEL_SETTINGS', {})
    apps_to_show = graph_settings.get('apps', [])

    #pylint: disable=E1101 
    
    
    
    classname_to_id = {}
    for app_ in apps_to_show:
        app = apps.get_app_config(app_)
        for model_name, model in app.models.items():
            classname_to_id[model.__name__] = get_id4model(app_, model_name)
            
    # print(classname_to_id)        

    weak_refs = {}
    
    class ASTClassFilter(ast.NodeVisitor):
        def __init__(self):
            self.names = []
    
        def generic_visit(self, node):
            obj = None
            if isinstance(node, ast.Name):
                obj = node.id
            elif isinstance(node, ast.Attribute):
                obj = node.attr
            # elif isinstance(node, ast.Alias):
            #     obj = node.name
            if obj and obj in classname_to_id:
                self.names.append(obj)
            ast.NodeVisitor.generic_visit(self, node)
    
    for app_ in apps_to_show:
        app = apps.get_app_config(app_)
        for model_name, model in app.models.items():
            src = inspect.getsource(model)
            tree = ast.parse(src)
            analyzer = ASTClassFilter()
            analyzer.visit(tree)
            weak_refs[model.__name__] = set(analyzer.names)
            # print(model.__name__, analyzer.names)

    nodes = []
    edges = []
    
    for app_ in apps_to_show:
        app = apps.get_app_config(app_)
        
        for model_name, model in app.models.items():
            # id_ = get_id4model(model.app_label, model.model)        
            # if not model.model_class():
            #     continue
            id_ = get_id4model(app_, model_name)        
    
        # for model in models:
    
            # doc_ = model.model_class().__doc__
            doc_ = model.__doc__
            title, body, metadata = utils.parse_docstring(doc_)
            if title:
                title = utils.parse_rst(title, None, None).strip()
                striptags = ["<p>", "</p>"]
                for tag in striptags:
                    if title.startswith(tag):
                        title = title[len(tag):]
                    if title.endswith(tag):
                        title = title[:-len(tag)]

            if body:
                body = utils.parse_rst(body, None, None)
            
            model_rstdoc = title + body
            
           
            label = "%s" % (model_name)
            fields = [f for f in model._meta.fields]
            many = [f for f in model._meta. many_to_many]
    
            fields_table = ''
            fields_table = '''
    <th><td><span style="background-color:#eeee00;color:#0000ff;font-size:22px;font-family:Candara">%s</span></td></th>
    ''' % model.__name__
    
            for field in fields:
                color = '#000000'
                if field.unique:
                    color = '#0000ff'
                fields_table += '''
            <tr><td><span style="color:%s;font-size:12px;font-family:Consolas;monospace">%s</span></td></tr>
                    ''' % (color, field.name)
    
            row_height = 14
            table_height = row_height * (len(fields) + 3) * 1.8
    
            imagesrc = '''
    <svg xmlns="http://www.w3.org/2000/svg" width="200px" height="''' + str(table_height) + '''px">
    <rect x="0" y="0" width="100%" height="100%" fill="#ffffff" stroke-width="20" stroke="#ffffff" ></rect>
        <foreignObject x="10" y="10" width="100%" height="100%" style="overflow: visible;">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-size:''' + str(row_height) + '''px">
        <table> ''' + fields_table + ''' </table> 
        </div>
        </foreignObject>
    </svg>
    '''  
    
            edge_color = {'inherit': 'from'}
            
            if model.__name__ == 'Course':
                pass
    
            for field_ in fields + many:
                if field_.remote_field:
                    rf_ = field_.remote_field
                    metaref = rf_.model._meta
                    if metaref.app_label != app_:
                        edge_color = {'inherit':'both'}
    
                    if rf_.model.__name__ in weak_refs[model.__name__]:
                        weak_refs[model.__name__].remove(rf_.model.__name__)        
    
                    edge = {
                            'from': id_,
                            'to':  get_id4model(metaref.app_label, metaref.model_name),
                                # "%s__%s" % (metaref.app_label, metaref.model_name),
                            'color': edge_color,
                           }
    
                    if str(field_.name).endswith('_ptr'):
                        #fields that end in _ptr are pointing to a parent object
                        edge.update({
                            'arrows': {'to': {'scaleFactor':0.75}}, #needed to draw from-to
                            'font':   {'align': 'middle'},
                            'label':  'is a',
                            'dashes': True
                            })
                    elif isinstance(field_, related.ForeignKey):
                        edge.update({
                                'arrows': {'to': {'scaleFactor':0.75}}
                            })
                    elif isinstance(field_, related.OneToOneField):
                        edge.update({
                                'font':  {'align': 'middle'},
                                'label': '|'
                            })
                    elif isinstance(field_, related.ManyToManyField):
                        edge.update({
                                'color':  {'color':'gray'},
                                'arrows': {'to': {'scaleFactor':1}, 'from': {'scaleFactor': 1}},
                            })
    
                    edges.append(edge)
                    
            for wr_ in weak_refs[model.__name__]:
                edge = {
                        'from': id_,
                        'to':  classname_to_id[wr_],
                        'color': 'red',
                        'dashes': True,
                        'physics': True,
                }
                edges.append(edge)
                
            title_ = get_template("dbmodel/dbnode.html").render(
                            {
                             'app_name': app_,  
                             'model_name': model.__name__,
                             'model_rstdoc': model_rstdoc.strip(),
                             'fields':fields,
                            }
                        )
            
                
            nodes.append(
                {
                    'id':    id_,
                    'label': label,
                    'imagesrc': imagesrc,
                    'shape': 'image',
                    'size':  table_height*1.8,
                    'group': app_,
                    'title': title_,
                }
            )

    data = {
        'nodes': json.dumps(nodes),
        'edges': json.dumps(edges)
    }
    return render(request, 'dbmodel/dbdiagram.html', data)
