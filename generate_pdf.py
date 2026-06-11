from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PANDUAN TEKNIS: SEGMENTASI PELANGGAN OLIST BRASIL', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Metode: RFM Analysis dengan K-Medoids (Varian CLARA)', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

    def code_block(self, code):
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 240)
        self.multi_cell(0, 5, code, 0, 'L', 1)
        self.ln(5)

pdf = PDF()
pdf.add_page()

# --- PENDAHULUAN ---
pdf.chapter_title("1. PENDAHULUAN")
pdf.chapter_body("Dokumen ini berisi panduan teknis per-baris kode untuk proyek segmentasi pelanggan Olist. Fokus utama adalah mengelompokkan pelanggan berdasarkan perilaku transaksi (RFM) menggunakan algoritma yang efisien untuk data besar (CLARA).")

# --- ROLE 1 ---
pdf.chapter_title("2. ROLE 1: DATA ARCHITECT & ENGINEER (MAHASISWA 1)")
pdf.chapter_body("Tanggung Jawab: Integrasi data, rekayasa fitur RFM, pembersihan data, dan optimasi nilai K.")

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, "A. Integrasi Data (Merging)", 0, 1)
pdf.code_block("df = orders.merge(customers, on='customer_id')\ndf = df.merge(payments, on='order_id')")
pdf.chapter_body("Penjelasan: Menggabungkan data pesanan dengan data demografi pelanggan melalui 'customer_id', lalu menggabungkannya dengan data pembayaran melalui 'order_id'. Menghasilkan satu tabel profil transaksi utuh.")

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, "B. RFM Engineering", 0, 1)
pdf.code_block("rfm = df.groupby('customer_unique_id').agg({\n    'order_purchase_timestamp': lambda x: (ref_date - x.max()).days,\n    'order_id': 'count',\n    'payment_value': 'sum'\n})")
pdf.chapter_body("Penjelasan: \n- Recency: Selisih hari antara tanggal referensi dengan transaksi terakhir.\n- Frequency: Jumlah total pesanan unik per pelanggan.\n- Monetary: Total akumulasi nilai pembayaran pelanggan.")

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, "C. Outlier & Scaling", 0, 1)
pdf.code_block("rfm_clean = rfm[~((rfm < (Q1 - 1.5 * IQR)) | (rfm > (Q3 + 1.5 * IQR))).any(axis=1)]\nrfm_scaled = scaler.fit_transform(rfm_clean)")
pdf.chapter_body("Penjelasan: Menghapus data pencilan (outlier) agar tidak menarik pusat klaster ke arah yang salah. Selanjutnya dilakukan standarisasi (Scaling) agar metrik hari (Recency) dan uang (Monetary) memiliki bobot yang sama dalam model.")

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, "D. Elbow Method", 0, 1)
pdf.code_block("rfm_sample = rfm_scaled_df.sample(n=10000)\nfor k in K_range:\n    kmedoids.fit(rfm_sample)")
pdf.chapter_body("Penjelasan: Menguji nilai K (2-8) menggunakan sampel 10.000 data. Titik 'siku' pada grafik menunjukkan jumlah klaster paling optimal yang meminimalkan inersia (jarak dalam kelompok).")

# --- PAGE 2 ---
pdf.add_page()
pdf.chapter_title("3. ROLE 2: MODEL ANALYST & STRATEGIST (MAHASISWA 2)")
pdf.chapter_body("Tanggung Jawab: Implementasi model klastering, audit kualitas, profil segmen, uji stabilitas, dan simulator.")

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, "A. Implementasi CLARA (K-Medoids for Big Data)", 0, 1)
pdf.code_block("final_model = CLARA(n_clusters=best_k, random_state=42)\nclusters = final_model.fit_predict(rfm_scaled)")
pdf.chapter_body("Penjelasan: Menggunakan algoritma CLARA untuk mengolah 94.000+ data secara efisien. CLARA bekerja dengan sampling berulang untuk menemukan medoids (pusat klaster) yang paling representatif.")

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, "B. Quality Audit (Silhouette Score)", 0, 1)
pdf.code_block("sil_score = silhouette_score(rfm_sample, final_model.predict(rfm_sample))")
pdf.chapter_body("Penjelasan: Mengukur seberapa baik pemisahan antar klaster. Nilai yang tinggi menandakan klaster sangat padat dan terpisah jauh dari klaster lain.")

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, "C. Profiling & Labelling", 0, 1)
pdf.code_block("cluster_names = {0: 'Champions', 1: 'Sultan', 2: 'At Risk', 3: 'Low Value'}\nrfm_clean['Segment'] = rfm_clean['Cluster'].map(cluster_names)")
pdf.chapter_body("Penjelasan: Memberikan label berdasarkan rata-rata nilai RFM. Contoh: Cluster dengan Monetary tinggi dan Recency rendah dinamakan 'Champions'.")

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, "D. Stability Testing (Jaccard Index)", 0, 1)
pdf.code_block("new_labels = new_model.fit_predict(data_noisy)\njaccard_score(original_labels, new_labels, average='macro')")
pdf.chapter_body("Penjelasan: Mengukur konsistensi klaster saat data diberikan gangguan (noise). Nilai Jaccard yang tinggi (>0.7) membuktikan model sangat stabil.")

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, "E. Simulator Aplikasi", 0, 1)
pdf.code_block("def predict_segment(r, f, m):\n    input_scaled = scaler.transform([[r, f, m]])\n    cluster = final_model.predict(input_scaled)[0]")
pdf.chapter_body("Penjelasan: Modul fungsional untuk mengklasifikasi pelanggan baru secara real-time berdasarkan input R, F, dan M, serta memberikan rekomendasi strategi pemasarannya.")

pdf.chapter_title("4. STRATEGI BISNIS REKOMENDASI")
pdf.chapter_body("- Champions: Program loyalty, akses awal produk baru.\n- Sultan: Penawaran produk premium, personal assistant.\n- At Risk: Email diskon win-back, survei kepuasan.\n- Low Value: Promo free shipping, voucher belanja minimal.")

pdf.output('Panduan_Teknis_Olist_Clustering.pdf')
