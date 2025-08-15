import streamlit as st
import pandas as pd
import os
import io # Dosya işlemleri için

# Streamlit uygulamasının başlığı
st.set_page_config(
    page_title="CSV'den Excel'e Dönüştürücü",
    page_icon="📄",
    layout="centered"
)

st.title("CSV'den Excel'e Dönüştürücü")
st.markdown("CSV dosyalarını sürükleyip bırakın veya seçin, otomatik olarak Excel'e dönüştürelim!")

def convert_csv_to_excel(csv_file_buffer, file_name):
    """
    Yüklenen CSV dosyasını okur ve Excel'e dönüştürür.
    file_name: Orijinal dosya adı (Excel adını oluşturmak için)
    """
    try:
        # CSV dosyasını Pandas DataFrame'e oku
        # Otomatik tür tanıma için dtype=None ve düşük bellek kullanımı için chunksize kullanabiliriz
        # Ancak streamlit'in upload_file objesi doğrudan tampon (buffer) sağlar,
        # bu da read_csv'ye doğrudan geçirilebilir.
        df = pd.read_csv(csv_file_buffer, dtype=None)
        
        # Excel dosyasını bellekte oluştur
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0) # Başa dön
        
        # Excel dosya adını oluştur
        excel_file_name = file_name.replace(".csv", ".xlsx")
        
        return True, excel_buffer, excel_file_name
    except Exception as e:
        return False, None, f"Dönüştürme hatası: {e}"

# Dosya yükleme alanı (sürükle-bırak destekli)
uploaded_files = st.file_uploader(
    "CSV Dosyalarını Buraya Sürükleyin veya Tıklayarak Seçin",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    st.subheader("Dönüştürülen Dosyalar:")
    for uploaded_file in uploaded_files:
        # Her bir dosya için dönüşüm yap
        success, output_buffer, output_name = convert_csv_to_excel(uploaded_file, uploaded_file.name)
        
        if success:
            st.success(f"'{uploaded_file.name}' başarıyla '{output_name}' olarak dönüştürüldü.")
            # İndirme butonu
            st.download_button(
                label=f"'{output_name}' İndir",
                data=output_buffer,
                file_name=output_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=output_name # Her butonun benzersiz bir anahtarı olmalı
            )
        else:
            st.error(f"'{uploaded_file.name}' dönüştürülürken bir hata oluştu: {output_name}")

st.info("İpucu: Birden fazla CSV dosyasını aynı anda yükleyebilirsiniz.")

st.markdown("---")
st.caption("Powered by Streamlit & Pandas")