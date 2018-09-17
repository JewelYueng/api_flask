from api import APP, DB
from flask import request, jsonify
from py2neo import Graph, Node, Relationship, walk, NodeMatcher, RelationshipMatcher, RelationshipMatch

@APP.route('/')
def index():
    return jsonify({'result': 'test'})

@APP.route('/entities', methods=['GET'])
def getEntities():
    type = request.args['type']
    entity_name = request.args['name']
    selector = NodeMatcher(DB)
    entities = selector.match(type, name=entity_name)
    result = []
    for en in entities:
        result.append({
            'name': en['name']
        })
    return jsonify(result)

@APP.route('/entityRels', methods=['GET'])
def getEntityRels():
    type = request.args['type']
    entity_name = request.args['name']
    rels = DB.run("MATCH p=(e:%s{name:'%s'})<-->() RETURN p"%(type, entity_name)).data()
    result = []
    # for r in rels:

@APP.route('/entityAttr')
def getEntityAttr():
    type = request.args['type']
    entity_name = request.args['name']
    results = DB.run("MATCH (e:%s{name:'%s'}) RETURN e"%(type, entity_name)).data()
    return jsonify(results)

@APP.route('/relations')
def getRelations():
    start_type = request.args['start_type']
    start_node = request.args['start_node']
    end_node = request.args['end_node']
    end_type = request.args['end_type']
    rel_type = request.args['rel_type']
    results = []
    r_matcher = RelationshipMatcher(DB)
    if rel_type and not start_type and not start_node and not end_node and not end_type:
        for re in r_matcher.match(r_type=rel_type):
            results.append({
                'start_node': re.start_node['name'],
                'end_node': re.end_node['name'],
                'attr': dict(re)
            })
        return jsonify(results)
    elif start_node or end_node:
        results = []
        if rel_type:
            matcher = RelationshipMatch(DB, r_type=rel_type)
        else:
            matcher = RelationshipMatch(DB)
        if start_node and end_node:
            for re in matcher.where('a.name="%s" AND b.name= "%s"' % (start_node, end_node)):
                results.append({
                    'start_node':re.start_node['name'],
                    'end_node': re.end_node['name'],
                    'attr': dict(re)
                })
        elif start_node and not end_node:
            for re in matcher.where('a.name="%s"' % start_node):
                results.append({
                    'start_node':re.start_node['name'],
                    'end_node': re.end_node['name'],
                    'attr': dict(re)
                })
        elif end_node and not start_node:
            for re in matcher.where('b.name= "%s"' % end_node):
                results.append({
                    'start_node':re.start_node['name'],
                    'end_node': re.end_node['name'],
                    'attr': dict(re)
                })
        return jsonify(results)
    else:
        return jsonify({
            'status': 'unfinished'
        })