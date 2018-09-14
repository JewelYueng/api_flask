from api import APP, DB
from flask import request, jsonify
from py2neo import Graph, Node, Relationship, walk, NodeMatcher

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
    if rel_type:
        for re in DB.run("MATCH p=()-[r:%s]->() RETURN p" % rel_type).data():
            w_re = walk(re)
            results.append({
                'start_node': w_re.start_node,
                'end_node': w_re.end_node,
                'attr': w_re
            })
    else:
        return jsonify({
            'status': 'unfinished'
        })