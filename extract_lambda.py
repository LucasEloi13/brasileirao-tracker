from datetime import datetime
from config.config_loader import load_config

from src.extract.competition_details_extractor import CompetitionDetailsExtractor # VAR
from src.load.S3Client import S3Client
from src.utils.s3_utils import gerar_s3_key


import logging

def lambda_handler(event, context):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        config = load_config()
        if not config:
            raise ValueError("Configuração não carregada corretamente.")
        else:
            logger.info("Configuração carregada com sucesso...")
    except Exception as e:
        logger.error(f"Erro ao carregar a configuração: {e}")

    try:
        extractor = CompetitionDetailsExtractor(config) # VAR
        data = extractor.get_competition_details() # VAR
        logger.info("Dados de competição extraídos com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao extrair dados de competição: {e}")
    
    try:
        # Classe S3Client
        s3 = S3Client(config)
        
        # Gera a chave S3 para o arquivo JSON
        s3_key = gerar_s3_key('raw', 'competition_details', 'json', datetime.now()) # VAR
        logger.info(f"Chave S3 gerada: {s3_key}")

        # Envia os dados para o S3
        s3.upload_json(data, s3_key)
        logger.info(f"Dados enviados para o S3 com a chave: {s3_key}")

        #deletar o teste
        s3.delete_object(s3_key)
        logger.info(f"Dados deletados do S3 com a chave: {s3_key}")
    except Exception as e:
        logger.error(f"Erro ao enviar dados para o S3: {e}")


# teste local
if __name__ == "__main__":
    # Simula o evento e contexto do Lambda
    event = {}
    context = None
    
    # Chama a função lambda_handler
    response = lambda_handler(event, context)
    print(response)