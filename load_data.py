import json
import os
from datetime import datetime
import requests
import logging
from tqdm import tqdm

# Configure logging
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f'pdbe_ligands_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # This will also print to console
    ]
)
logger = logging.getLogger(__name__)

def get_url(url):
    """
    Makes a request to a URL. Returns a JSON of the results or empty dict if no response
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

BASE_URL = "https://www.ebi.ac.uk/pdbe/"  # the beginning of the URL for PDBe's API.
PDBEKB_UNIPROT_URL = BASE_URL + "graph-api/uniprot/"

def get_ligand_site_data(uniprot_accession):
    """
    Retrieve ligand site data for a given UniProt accession and parse it into list.
    """
    if not uniprot_accession:
        # logger.warning("No UniProt accession provided")
        return []

    url = PDBEKB_UNIPROT_URL + "ligand_sites/" + uniprot_accession
    # logger.info(f"Fetching ligand data for {uniprot_accession} from {url}")
    
    data = get_url(url=url)
    data_to_ret = []

    if not data:
        # logger.warning(f"No data returned for {uniprot_accession}")
        return []

    for data_uniprot_accession in data:
        accession_data = data.get(data_uniprot_accession)
        if not accession_data or 'data' not in accession_data:
            # logger.warning(f"No valid data found for accession {data_uniprot_accession}")
            continue

        for row in accession_data['data']:
            ligand_accession = row.get('accession')
            name = row.get('name')
            if not ligand_accession or not name:
                # logger.warning(f"Missing ligand accession or name in data: {row}")
                continue

            # Get the number of atoms in the ligand
            num_atoms = row.get('additionalData', {}).get('numAtoms', 0)
            lig_data = dict()
            ligand_accession_set = set()

            for residue in row.get("residues", []):
                if ligand_accession not in ligand_accession_set:
                    ligand_accession_set.add(ligand_accession)
                    lig_data['ligand_accession'] = ligand_accession
                    lig_data['ligand_name'] = name
                    lig_data['ligand_num_atoms'] = num_atoms
                    lig_data['pdb'] = residue.get('allPDBEntries', [''])[0] if residue.get('allPDBEntries') else ''
                    data_to_ret.append(lig_data)
                    # logger.debug(f"Added ligand data: {lig_data}")


    return data_to_ret


def update_data(dis_file):
    with open(dis_file, 'r') as file:
        idp_data = json.load(file)
        if isinstance(idp_data, dict) and "data" in idp_data:
            simplified_data = []
            for item in tqdm(idp_data["data"]):
                if isinstance(item, dict):
                    uniprot_id = item.get('acc')
                    if uniprot_id:
                        ligands = get_ligand_site_data(uniprot_id)
                        if ligands:
                            simplified_doc = {
                            'uniprot_id': uniprot_id,
                            'name': item.get('name'),
                            'disprot_id': item.get('disprot_id'),
                            'ligands': ligands
                        }
                            simplified_data.append(simplified_doc)
            
            with open('IDPLig_app/data/update_data.json', 'w') as f:
                json.dump(simplified_data, f, indent=4)


if __name__ == "__main__":
    update_data('IDPLig_app/data/DisProt.json') 