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

# 获取某个实体的所有关系，包括指向他的以及他指向的。
@APP.route('/entityRels', methods=['GET'])
def getEntityRels():
    type = request.args['type']
    entity_name = request.args['name']
    # 获取特定的节点
    node = NodeMatcher(DB).match(type, name = entity_name).first()
    # 获取该节点的所有关系
    rel_matcher = RelationshipMatcher(DB)
    rels = rel_matcher.match(nodes = set([node, None]))
    result = []
    for re in rels:
        result.append({
            'start_node': re.start_node,
            'end_node': re.end_node,
            'path': str(re),
            'attr': dict(re)
        })
    return jsonify(result)

# 获取特定实体的属性
@APP.route('/entityAttr')
def getEntityAttr():
    type = request.args['type']
    entity_name = request.args['name']
    results = []
    for n in NodeMatcher(DB).match(type, name=entity_name):
        results.append(dict(n))
    return jsonify(results)

#获取满足条件的关系信息
@APP.route('/relations')
def getRelations():
    start_type = request.args['start_type']
    start_node = request.args['start_node']
    end_node = request.args['end_node']
    end_type = request.args['end_type']
    rel_type = request.args['rel_type']
    results = []
    r_matcher = RelationshipMatcher(DB)
    # 条件0： 没有给出任何信息
    if not rel_type and not start_type and not start_node and not end_node and not end_type:
        return jsonify({
            'code': '1001',
            'msg': 'no messages'
        })
    # 条件1：没给出开始节点和结束节点的任何信息，但给出关系类型
    elif rel_type and not start_type and not start_node and not end_node and not end_type:
        for re in r_matcher.match(r_type=rel_type):
            results.append({
                'start_node': re.start_node['name'],
                'end_node': re.end_node['name'],
                'attr': dict(re)
            })
        return jsonify(results)
    # 条件2：给出了开始节点或者结束节点
    elif start_node or end_node:
        results = []
        # 条件2.1： 并且给出关系类型
        if rel_type:
            matcher = RelationshipMatch(DB, r_type=rel_type)
        # 条件2.2：没有给出关系类型
        else:
            matcher = RelationshipMatch(DB)
        # 条件2.3：同时给出了开始节点和结束节点
        if start_node and end_node:
            for re in matcher.where('a.name="%s" AND b.name= "%s"' % (start_node, end_node)):
                results.append({
                    'start_node':re.start_node['name'],
                    'end_node': re.end_node['name'],
                    'attr': dict(re)
                })
        # 条件2.4：只存在开始节点，没有结束节点
        elif start_node and not end_node:
            for re in matcher.where('a.name="%s"' % start_node):
                results.append({
                    'start_node':re.start_node['name'],
                    'end_node': re.end_node['name'],
                    'attr': dict(re)
                })
        # 条件2.5：只存在结束节点不存在开始节点
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
            'code': '1002',
            'msg': 'error messages'
        })