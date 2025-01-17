import uuid
from collections import defaultdict
import pprint

def group_graph(result_graph, request):
    # Minimum number of duplicate edges for grouping nodes together
    MINIMUM_EDGES_TO_COLLAPSE = 2

    # Get all unique edge types specified in the query
 
    edge_types = list(set(e['data']['edgeType'] for e in request['requests']['edges']))
    # print("edge type ---------------------------------------",edge_types)
    # For each edge type, determine the best grouping (source or target)
    edge_groupings = []
    for edge_type in edge_types:
        edges_of_type = [e for e in result_graph['edges'] if e['data']['label'] == edge_type]
        source_groups = defaultdict(list)
        target_groups = defaultdict(list)

        for edge in edges_of_type:
            source_groups[edge['data']['source']].append(edge)
            target_groups[edge['data']['target']].append(edge)

        # Compare which grouping has fewer groups
        grouped_by = "target" if len(target_groups) < len(source_groups) else "source"
        groups = target_groups if grouped_by == "target" else source_groups

        edge_groupings.append({
            "count": len(edges_of_type),
            "edgeType": edge_type,
            "groupedBy": grouped_by,
            "groups": groups
        })
          
    edge_groupings.sort(
        key=lambda g: g['count'] - len(g['groups']),
        reverse=True
    )
    print("sorted edge grouping",edge_groupings)
   
    new_graph = {
        "nodes": result_graph['nodes'][:],
        "edges": result_graph['edges'][:]
    }


 
    for grouping in edge_groupings:
        sorted_groups = sorted(grouping['groups'].items(), key=lambda g: len(g[1]), reverse=True)






        node_count_by_label={}
        for key, edges in sorted_groups:
            print("key___________________________________))))))))))",key)
            print("edge",edge)
            if len(edges) < MINIMUM_EDGES_TO_COLLAPSE:
                continue

          
            child_node_ids = [
                edge['data']['source'] if grouping['groupedBy'] == "target" else edge['data']['target']
                for edge in edges
            ]
            print("Child_node_id",child_node_ids)
 
            child_nodes = [node for node in new_graph['nodes'] if node['data']['id'] in child_node_ids]
            parents_of_child_nodes = list({node['data'].get('parent') for node in child_nodes})


            counts = defaultdict(lambda: defaultdict(int))

           
 
        
            if len(parents_of_child_nodes) > 1:
                continue
 
        
            if parents_of_child_nodes[0]:
                all_child_nodes_of_parent = [
                    node for node in new_graph['nodes']
                    if node['data'].get('parent') == parents_of_child_nodes[0]
                ]
                
                if len(all_child_nodes_of_parent) == len(child_nodes):
                    add_new_edge(new_graph, edges, grouping, parents_of_child_nodes[0])
                    continue
                print("all child of nodes",all_child_nodes_of_parent)
             
            parent_id = f"n{uuid.uuid4().hex}"
            parent_node = {"data": {"id": parent_id, "type": "parent", "parent": parents_of_child_nodes[0]}}

            new_graph['nodes'].append(parent_node)
            for node in new_graph['nodes']:
                if node['data']['id'] in child_node_ids:
                    node['data']['parent'] = parent_id

            add_new_edge(new_graph, edges, grouping, parent_id)
    counts_by_parent = defaultdict(lambda: defaultdict(int))
    # count the edge based on the  parent id 


    for node in new_graph['nodes']:
      
        node_type = node['data'].get('type')
        parent_id = node['data'].get('parent')

         
        if parent_id:
            counts_by_parent[parent_id][node_type] += 1

     
    result = {parent: dict(types) for parent, types in counts_by_parent.items()}

    # Print the result
    print("Count the value based on the parent  ",result)
    return new_graph

def add_new_edge(graph, edges, grouping, parent_id):
    new_edge_id = f"e{uuid.uuid4().hex}"
    new_edge = {
        "data": {
            **edges[0]['data'],
            "id": new_edge_id,
            grouping['groupedBy']: parent_id
        }
    }

    graph['edges'] = [
        edge for edge in graph['edges']
        if not any(
            edge['data']['label'] == e['data']['label'] and
            edge['data']['source'] == e['data']['source'] and
            edge['data']['target'] == e['data']['target']
            for e in edges
        )
    ]
    graph['edges'].append(new_edge)

if __name__ == "__main__":
    oldGraph = {
	"nodes": [
		{
			"data": {
				"id": "transcript enst00000456328",
				"type": "transcript",
				"name": "DDX11L2-202"
			}
		},
		{
			"data": {
				"id": "gene ensg00000290825",
				"type": "gene",
				"name": "DDX11L2"
			}
		},
		{
			"data": {
				"id": "exon ense00002312635",
				"type": "exon",
				"name": "exon ense00002312635"
			}
		},
		{
			"data": {
				"id": "exon ense00002234944",
				"type": "exon",
				"name": "exon ense00002234944"
			}
		},
		{
			"data": {
				"id": "exon ense00003582793",
				"type": "exon",
				"name": "exon ense00003582793"
			}
		},
		{
			"data": {
				"id": "transcript enst00000384476",
				"type": "transcript",
				"name": "RNVU1-15-201"
			}
		},
		{
			"data": {
				"id": "gene ensg00000207205",
				"type": "gene",
				"name": "RNVU1-15"
			}
		},
		{
			"data": {
				"id": "exon ense00001808588",
				"type": "exon",
				"name": "exon ense00001808588"
			}
		},
		{
			"data": {
				"id": "transcript enst00000364938",
				"type": "transcript",
				"name": "SNORA73A-201"
			}
		},
		{
			"data": {
				"id": "gene ensg00000274266",
				"type": "gene",
				"name": "SNORA73A"
			}
		},
		{
			"data": {
				"id": "exon ense00001439701",
				"type": "exon",
				"name": "exon ense00001439701"
			}
		},
		{
			"data": {
				"id": "transcript enst00000426952",
				"type": "transcript",
				"name": "HNRNPCP9-201"
			}
		},
		{
			"data": {
				"id": "gene ensg00000232048",
				"type": "gene",
				"name": "HNRNPCP9"
			}
		},
		{
			"data": {
				"id": "exon ense00001800064",
				"type": "exon",
				"name": "exon ense00001800064"
			}
		},
		{
			"data": {
				"id": "transcript enst00000450305",
				"type": "transcript",
				"name": "DDX11L1-201"
			}
		},
		{
			"data": {
				"id": "gene ensg00000223972",
				"type": "gene",
				"name": "DDX11L1"
			}
		},
		{
			"data": {
				"id": "exon ense00001863096",
				"type": "exon",
				"name": "exon ense00001863096"
			}
		},
		{
			"data": {
				"id": "exon ense00001758273",
				"type": "exon",
				"name": "exon ense00001758273"
			}
		},
		{
			"data": {
				"id": "exon ense00001671638",
				"type": "exon",
				"name": "exon ense00001671638"
			}
		},
		{
			"data": {
				"id": "exon ense00001948541",
				"type": "exon",
				"name": "exon ense00001948541"
			}
		}
	],
	"edges": [
		{
			"data": {
				"edge_id": "transcript_transcribed_from_gene",
				"label": "transcribed_from",
				"source": "transcript enst00000456328",
				"target": "gene ensg00000290825"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000456328",
				"target": "exon ense00002312635"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000456328",
				"target": "exon ense00002234944"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000456328",
				"target": "exon ense00003582793"
			}
		},
		{
			"data": {
				"edge_id": "transcript_transcribed_from_gene",
				"label": "transcribed_from",
				"source": "transcript enst00000384476",
				"target": "gene ensg00000207205"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000384476",
				"target": "exon ense00001808588"
			}
		},
		{
			"data": {
				"edge_id": "transcript_transcribed_from_gene",
				"label": "transcribed_from",
				"source": "transcript enst00000364938",
				"target": "gene ensg00000274266"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000364938",
				"target": "exon ense00001439701"
			}
		},
		{
			"data": {
				"edge_id": "transcript_transcribed_from_gene",
				"label": "transcribed_from",
				"source": "transcript enst00000426952",
				"target": "gene ensg00000232048"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000426952",
				"target": "exon ense00001800064"
			}
		},
		{
			"data": {
				"edge_id": "transcript_transcribed_from_gene",
				"label": "transcribed_from",
				"source": "transcript enst00000450305",
				"target": "gene ensg00000223972"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000450305",
				"target": "exon ense00001863096"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000450305",
				"target": "exon ense00001758273"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000450305",
				"target": "exon ense00001671638"
			}
		},
		{
			"data": {
				"edge_id": "transcript_includes_exon",
				"label": "includes",
				"source": "transcript enst00000450305",
				"target": "exon ense00001948541"
			}
		}
	],
	"node_count": 1113487,
	"edge_count": 1902311,
	"node_count_by_label": [
		{
			"count": 252835,
			"label": "transcript"
		},
		{
			"count": 62700,
			"label": "gene"
		},
		{
			"count": 797952,
			"label": "exon"
		}
	],
	"edge_count_by_label": [
		{
			"count": 252835,
			"relationship_type": "transcribed_from"
		},
		{
			"count": 1649476,
			"relationship_type": "includes"
		}
	],
	"title": "Relationships between transcripts, genes, and exons",
	"summary": "**Key Trends and Relationships:**\n\nThe graph data reveals a hierarchical relationship between genes, exons, and transcripts. Genes are transcribed into transcripts, which in turn include exons. This hierarchical structure is essential for understanding the flow of genetic information from DNA to RNA to protein.\n\n**Important Metrics:**\n\nThe graph contains 5 source nodes (genes), 10 target nodes (exons), and 11 edges (relationships). This relatively small size allows for easy visualization and analysis of the data.\n\n**Central Nodes:**\n\nThere are no central nodes in the graph, as all genes have only one transcript and each transcript includes only a few exons. This suggests that the genes in this dataset are not highly interconnected and may function independently.\n\n**Notable Structures:**\n\nThe graph does not exhibit any notable structures such as chains, hubs, or clusters. This is likely due to the small size and simple structure of the data.\n\n**Specific Characteristics:**\n\nThe data does not provide information about alternative splicing or regulatory mechanisms. However, the hierarchical structure of the graph suggests that alternative splicing may occur, as different transcripts can include different combinations of exons.\n\n**Notable Relationships:**\n\nThere are no notable relationships between nodes with a higher number of associated related nodes or complex processes. This is likely due to the small size and simple structure of the data.",
	"annotation_id": "67823527ae281b89a61fa243",
	"created_at": "2025-01-11T12:08:55.676000",
	"updated_at": "2025-01-11T12:08:55.676000"
}
    request = {
    "requests": {
        "nodes": [
        {
            "data": {
            "node_id": "n1",
            "id": "",
            "type": "transcript",
            "properties": {}
            }
        },
        {
            "data": {
            "node_id": "n2",
            "id": "",
            "type": "gene",
            "properties": {}
            }
        },
        {
            "data": {
            "node_id": "n3",
            "id": "",
            "type": "exon",
            "properties": {}
            }
        }
        ],
        "edges": [
        {
            "data": {
            "predicate_id": "p1",
            "edgeType": "transcribed from",
            "source": "n1",
            "target": "n2"
            }
        },
        {
            "data": {
            "predicate_id": "p2",
            "edgeType": "includes",
            "source": "n1",
            "target": "n3"
            }
        }
        ]
    }
    }


    grouped_graph = group_graph(oldGraph, request)
    pprint.pprint(grouped_graph, depth=None)
