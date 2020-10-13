import numpy as np

def populations(chrom, panel_file):
    with open(panel_file, "rt") as f:
        next(f)
        rows = (line.strip().split("\t") for line in f)
        sample_map = {sample_id: (pop, superpop) for sample_id, pop, superpop, _ in rows}
    
    # map each 1kg sample id ts nodes
    import json
    
    samples_to_nodes = {
        json.loads(ind.metadata)["individual_id"]: ind.nodes for ind in chrom.individuals()
    }
    
    superpops = {}
    pops = {}
    for sample_id, (p, sp) in sample_map.items():
        pops.setdefault(p, [])
        superpops.setdefault(sp, [])
        nid = samples_to_nodes[sample_id]
        pops[p].append(nid)
        superpops[sp].append(nid)
    
    for p in pops:
        pops[p] = np.concatenate(pops[p]).reshape(-1)
    for sp in superpops:
        superpops[sp] = np.concatenate(superpops[sp]).reshape(-1)

    return pops, superpops
