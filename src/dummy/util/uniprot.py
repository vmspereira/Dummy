"""Uses unitprot to retreive data related to proteins."""
import json

import xmlschema


schema = xmlschema.XMLSchema('https://www.uniprot.org/docs/uniprot.xsd')


def retreive(protein, format='json'):
    """Retreives a protein function, pathways and EC.

    Args:
        protein ([type]): The protein
        format (str, optional): Format . Defaults to 'json'.

    Returns:
        A dictionary or a json string
    """
    func = ''
    act = []
    pw = None

    entry_dict = schema.to_dict(
        f"https://www.uniprot.org/uniprot/{protein}.xml")
    content = entry_dict['entry'][0]
    for x in content['comment']:
        if x['@type'] == 'function':
            try:
                func = x['text'][0]['$']
            except Exception:
                func = x['text'][0]
        elif x['@type'] == 'catalytic activity':
            s = x['reaction']['text']
            db_reference = x['reaction']['dbReference']
            for y in db_reference:
                if y['@type'] == 'EC':
                    s += f" ({y['@id']})"
            act.append(s)
        elif x['@type'] == 'pathway':
            pw = x['text']
    if format == 'json':
        res = json.dumps({'function': func, 'activity': act, 'pathway': pw})
    else:
        res = {'function': func, 'activity': act, 'pathway': pw}
    return res
