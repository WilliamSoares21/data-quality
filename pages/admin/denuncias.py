# pages/admin/denuncias.py
import streamlit as st
from pymongo import MongoClient

def get_database():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client["cluster-data-quality"]

def visualizar_denuncias():
    st.title("Visualização de Denúncias")
    
    db = get_database()
    denuncias_collection = db["denuncias"]
    
    denuncias = list(denuncias_collection.find())
    if denuncias:
        for denuncia in denuncias:
            with st.expander(f"Denúncia de {denuncia['denunciante']} contra {denuncia['denunciado']}"):
                st.write(f"**Motivo:** {denuncia['motivo']}")
                st.write(f"**Data:** {denuncia['data']}")
                st.write(f"**Status:** {denuncia['status']}")
                if denuncia['status'] == 'recusada':
                    st.write(f"**Comentário do Admin:** {denuncia['comentario_admin']}")
                if denuncia['status'] == 'em_analise':
                    if st.button("Aprovar", key=f"aprovar_{denuncia['_id']}"):
                        denuncias_collection.update_one({"_id": denuncia["_id"]}, {"$set": {"status": "aceita"}})
                        st.rerun()
                    if st.button("Rejeitar", key=f"rejeitar_{denuncia['_id']}"):
                        comentario = st.text_area("Comentário do Admin", key=f"comentario_{denuncia['_id']}")
                        if comentario:
                            denuncias_collection.update_one({"_id": denuncia["_id"]}, {"$set": {"status": "recusada", "comentario_admin": comentario}})
                            st.rerun()
    else:
        st.info("Nenhuma denúncia registrada ainda.")

visualizar_denuncias()