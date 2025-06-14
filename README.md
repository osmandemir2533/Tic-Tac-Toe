# Tic-Tac-Toe

Tic-Tac-Toe, Python (Flask) ile geliştirilmiş, modern ve kullanıcı dostu bir web uygulamasıdır.  
Oyun, hem tek oyunculu (AI ile) hem de iki oyunculu modda oynanabilir.  
Proje, modern web teknolojileri ve en iyi kullanıcı deneyimi pratikleri ile geliştirilmiştir.

## 🎮 Canlı Demo

Oyunu hemen oynamak için: [https://tic-tac-toe-2fjq.onrender.com](https://tic-tac-toe-2fjq.onrender.com)

---

## ❓ Nasıl Oynanır
  
• Tahta boyutunu 3x3 ile 10x10 arasında seçin.  
• Oyun modunu belirleyin:  
|__ Bilgisayara karşı (AI ile)  
|__ İki kişilik mod                
• İlk hamleyi kim yapacaksa seçin.  
• "Başla" butonuna tıklayarak oyunu başlatın.  
• Sıranız geldiğinde tahtadaki boş hücreye tıklayın.  
• Satır, sütun veya çaprazda kazanan kombinasyonu yapmaya çalışın.  
• Oyun berabere biterse veya biri kazanırsa sonucu görebilirsiniz.  
• Yeniden oynamak için "Yeniden Oyna" butonuna basın.
> Amaç, yatay, dikey veya çapraz olarak aynı sembolü arka arkaya yerleştirmektir. Aynı sembolleri sırasıyla yerleştiren oyuncu oyunu kazanır.

---

## 🚀 Projeyi Çalıştırmak İçin

### Gereksinimler

Projeyi çalıştırmak için aşağıdaki yazılımların yüklü olması gerekmektedir:

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Kurulum

1. **Repoyu klonlayın**
```bash
git clone https://github.com/osmandemir2533/Tic-Tac-Toe.git
cd Tic-Tac-Toe
```

2. **Gerekli paketleri yükleyin**
```bash
pip install -r requirements.txt
```

3. **Uygulamayı başlatın**
```bash
python app.py
```

Uygulama varsayılan olarak `http://localhost:5000` adresinde çalışacaktır.

---

## 🎮 Oyun Özellikleri

### Oyun Modları

1. **Tek Oyunculu Mod (AI ile)**
   - Kullanıcı, yapay zeka ile karşı karşıya oynar
   - İlk başlama sırası seçilebilir
   - AI, minimax algoritması ile en iyi hamleyi hesaplar
   - Oyun sonunda kazanan veya beraberlik durumu gösterilir

2. **İki Oyunculu Mod**
   - İki oyuncu aynı cihazda sırayla oynar
   - X ve O sırasıyla oynar
   - Oyun sonunda kazanan veya beraberlik durumu gösterilir

### Tahta Boyutu

- Oyun tahtası boyutu 3x3 ile 10x10 arasında ayarlanabilir
- Varsayılan boyut 3x3'tür
- Her boyut için kazanma koşulları otomatik hesaplanır

### Kullanıcı Arayüzü

- Modern ve responsive tasarım
- Mobil cihazlara uyumlu arayüz
- Kolay kullanılabilir menü sistemi
- Oyun durumu göstergeleri
- Yükleme animasyonları

## 🖥️ Arayüz ve Ekran Görüntüleri

### Ana Sayfa (index.html)
Ana sayfa, oyunun başlangıç noktasıdır. Burada oyuncular:
- Tahta boyutunu seçebilir (3x3 ile 10x10 arası)
- İlk başlama sırasını belirleyebilir
- AI ile oynamayı veya iki kişilik modu seçebilir

> ![Ana Sayfa](https://github.com/user-attachments/assets/91e0000a-8b34-4639-9495-d53cceca65b1)

### AI Oyun Sayfası (game.html)
AI ile oyun modunda kullanılan sayfa. Özellikler:
- Dinamik oyun tahtası
- AI düşünme animasyonu
- Kazanma/beraberlik bildirimleri
- Yeniden oynama seçeneği

> ![AI Oyun Sayfası](https://github.com/user-attachments/assets/2022587f-3222-4574-be67-99d84ed9b902)

### İki Kişilik Oyun Sayfası (twoplayer.html)
İki oyuncunun aynı cihazda oynayabileceği mod. Özellikler:
- Sıra göstergesi
- Dinamik tahta
- Kazanma/beraberlik bildirimleri
- Yeniden oynama seçeneği

> ![İki Kişilik Oyun](https://github.com/user-attachments/assets/e0b05722-34d1-4dbb-8de8-aead74b7d8c1)

### Hakkında Sayfası (about.html)
Projenin detaylı açıklamalarını içeren sayfa:
- Proje hakkında genel bilgiler
- Kullanılan teknolojiler
- Algoritma açıklamaları
- Geliştirici bilgileri

> ![Hakkında Sayfası](https://github.com/user-attachments/assets/e81111e9-f809-4675-8a4f-0331ba7f039b)

### İletişim Sayfası (contact.html)
Geliştirici ile iletişim kurulabilecek sayfa:
- Geliştirici bilgileri
- Sosyal medya bağlantıları
- İletişim formu

> ![İletişim Sayfası](https://i.imgur.com/HxZkkhh.png)

### Mobil Uyumluluk
Tüm sayfalar responsive tasarıma sahiptir:
- Mobil cihazlarda optimize görünüm
- Touch-friendly butonlar
- Dinamik menü sistemi
- Esnek tahta boyutlandırma

<p align="center">
  <img src="https://github.com/user-attachments/assets/478f1763-56ba-4fee-8bce-a3376fbef6f4" width="300" />
  <img src="https://github.com/user-attachments/assets/be6191b7-9f06-460a-a8ff-33cb0dd2162b" width="300" />
  <img src="https://github.com/user-attachments/assets/896014ac-cfcf-4a91-9f0d-521c0298af33" width="317" />
</p>


### Oyun İçi Ayrıntılar / Arayüz
Tahta boyutları için örnek görünüm:

> <img src="https://github.com/user-attachments/assets/8cf85781-6cf3-463f-8aa2-d17d2ae13d7d" width="480" />

Çeşitli oyun durumları için bildirimler:

> ![Kazanma Bildirimi](https://github.com/user-attachments/assets/20845ac9-6994-402d-b315-4a6360f77154)

> ![Erken Beraberlik Bildirimi](https://github.com/user-attachments/assets/b9b73dc4-696b-46fb-8284-d7c4cb8b74c5)

> <img src="https://github.com/user-attachments/assets/0070b215-4445-44a6-b9b2-9459eed0a53b" width="480" />

---

## 🧠 Algoritma ve Oyun Mantığı

### Minimax Algoritması

Minimax, iki oyunculu sıfır toplamlı oyunlarda (zero-sum games) kullanılan bir karar verme algoritmasıdır. Tic-Tac-Toe'da AI'nin en iyi hamleyi seçmesini sağlar.

#### Algoritmanın Çalışma Prensibi

1. **Ağaç Yapısı**
   - Her hamle bir düğüm (node) olarak temsil edilir
   - Her düğüm, oyunun o anki durumunu gösterir
   - Ağaç, tüm olası hamleleri ve sonuçlarını içerir

2. **Değerlendirme Fonksiyonu**
   ```python
   def evaluate(board):
       if check_win(board, 'X'):  # AI kazanırsa
           return 1
       elif check_win(board, 'O'):  # İnsan kazanırsa
           return -1
       elif is_board_full(board):  # Beraberlik
           return 0
       return None  # Oyun devam ediyor
   ```

3. **Minimax Fonksiyonu**
   ```python
   def minimax(board, depth, is_maximizing):
       score = evaluate(board)
       if score is not None:
           return score

       if is_maximizing:
           best_score = float('-inf')
           for move in get_empty_cells(board):
               board[move] = 'X'
               score = minimax(board, depth + 1, False)
               board[move] = ' '
               best_score = max(score, best_score)
           return best_score
       else:
           best_score = float('inf')
           for move in get_empty_cells(board):
               board[move] = 'O'
               score = minimax(board, depth + 1, True)
               board[move] = ' '
               best_score = min(score, best_score)
           return best_score
   ```

4. **Derinlik Sınırlaması**
   - Büyük tahtalarda (4x4 ve üzeri) performans için derinlik sınırlaması uygulanır
   - Varsayılan derinlik: 3 hamle
   - Derinlik sınırı, tahta boyutuna göre dinamik olarak ayarlanır

### Monte Carlo Tree Search (MCTS)

Büyük tahtalarda (6x6 ve üzeri) Minimax yerine MCTS kullanılır. MCTS, daha az hesaplama gerektiren ve büyük durum uzaylarında daha iyi performans gösteren bir algoritmadır.

#### MCTS'in Çalışma Prensibi

1. **Seçim (Selection)**
   - Ağaçta en umut verici düğümü seçer
   - UCB1 (Upper Confidence Bound) formülü kullanılır:
   ```
   UCB1 = (w/n) + c * sqrt(ln(t)/n)
   ```
   - w: kazanma sayısı
   - n: ziyaret sayısı
   - t: toplam simülasyon sayısı
   - c: keşif parametresi (genelde 1.41)

2. **Genişleme (Expansion)**
   - Seçilen düğümden yeni bir hamle ekler
   - Rastgele bir boş hücre seçilir

3. **Simülasyon (Simulation)**
   - Yeni durumdan oyun sonuna kadar rastgele hamleler yapılır
   - Sonuç (kazanma/kaybetme/beraberlik) kaydedilir

4. **Geri Yayılım (Backpropagation)**
   - Simülasyon sonucu ağaçta yukarı doğru yayılır
   - Her düğümün istatistikleri güncellenir

### Kazanma Koşulları

1. **Standart Tahta (3x3)**
   - Yatay, dikey veya çapraz 3 işaret
   - 8 farklı kazanma kombinasyonu

2. **Büyük Tahtalar (4x4 ve üzeri)**
   - Dinamik kazanma koşulları
   - Tahta boyutuna göre minimum işaret sayısı:
     - 4x4: 4 işaret
     - 5x5: 4 işaret
     - 6x6 ve üzeri: 5 işaret

3. **Beraberlik Durumu**
   - Tüm hücreler dolu ve kazanan yoksa
   - Kalan hamle sayısı kazanma için yetersizse

### Hamle Sırası ve Stratejiler

1. **İlk Hamle**
   - AI ilk başlıyorsa:
     - 3x3: Köşe veya merkez
     - 4x4 ve üzeri: Merkez bölge
   - İnsan ilk başlıyorsa:
     - İnsanın hamlesine göre en iyi karşı hamle

2. **Orta Oyun Stratejileri**
   - Saldırı: Kazanma fırsatı varsa
   - Savunma: Rakibin kazanma tehdidi varsa
   - Kontrol: Merkez ve köşeleri kontrol etme

3. **Son Oyun**
   - Kazanma fırsatı değerlendirmesi
   - Beraberlik stratejisi
   - Son hamle optimizasyonu

### Performans Optimizasyonları

1. **Alpha-Beta Budama**
   - Gereksiz ağaç dallarını atlar
   - Hesaplama süresini önemli ölçüde azaltır

2. **Önbellek (Cache)**
   - Daha önce hesaplanan durumlar saklanır
   - Tekrarlanan hesaplamalar önlenir

3. **Paralel İşleme**
   - Büyük tahtalarda çoklu işlemci kullanımı
   - Hamle hesaplama süresini kısaltır

### Oyun Durumu Yönetimi

1. **Tahta Temsili**
   ```python
   board = [[' ' for _ in range(size)] for _ in range(size)]
   ```

2. **Hamle Doğrulama**
   ```python
   def is_valid_move(board, row, col):
       return 0 <= row < len(board) and \
              0 <= col < len(board) and \
              board[row][col] == ' '
   ```

3. **Kazanma Kontrolü**
   ```python
   def check_win(board, player):
       size = len(board)
       # Yatay kontrol
       for row in board:
           if all(cell == player for cell in row):
               return True
       
       # Dikey kontrol
       for col in range(size):
           if all(board[row][col] == player for row in range(size)):
               return True
       
       # Çapraz kontrol
       if all(board[i][i] == player for i in range(size)):
           return True
       if all(board[i][size-1-i] == player for i in range(size)):
           return True
       
       return False
   ```

---

## 🛠️ Kullanılan Teknolojiler

- **Backend:**
  - Python 3.8+
  - Flask (Web Framework)
  - Minimax Algoritması (AI için)
  - Monte Carlo Tree Search (Büyük tahtalar için)

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript
  - Responsive Design

- **Diğer:**
  - Flask-Session (Oturum yönetimi)
  - Flask-Flash (Bildirimler)

---

## 📁 Proje Yapısı

```
Flask-Tic-Tac-Toe/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── about.html
│   ├── contact.html
│   ├── game.html
│   ├── index.html
│   └── twoplayer.html
│
├── app.py
├── requirements.txt
└── README.md
```

---

### Render'da Deploy Deneyimi

Projeyi Render'da deploy etmek için şu adımları izledim:

1. Öncelikle projeye gerekli production dosyalarını ekledim:
   - `gunicorn` paketini yükledim: `pip install gunicorn`
   - `requirements.txt` dosyasını güncelledim
   - `Procfile` oluşturdum ve içine `web: gunicorn app:app` yazdım

2. [Render.com](https://render.com)'da yeni bir hesap oluşturdum

3. Dashboard'da "New +" butonuna tıklayıp "Web Service" seçtim

4. GitHub repomu bağladım ve Tic-Tac-Toe projemi seçtim

5. Deploy ayarlarını şu şekilde yaptım:
   - Name: tic-tac-toe
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Plan: Free

6. "Create Web Service" butonuna tıkladım

7. Render otomatik olarak GitHub repomdan kodu çekti ve deploy etti

8. Birkaç dakika sonra uygulamam canlıya alındı ve şu adresten erişilebilir oldu:
   [https://tic-tac-toe-2fjq.onrender.com](https://tic-tac-toe-2fjq.onrender.com)

Deploy sırasında dikkat ettiğim noktalar:
- Flask uygulamasının production ortamında çalışması için `gunicorn` kullanmak önemli
- `requirements.txt` dosyasında tüm bağımlılıkların doğru versiyonlarla belirtilmesi gerekiyor
- `Procfile` dosyası, Render'a uygulamanın nasıl başlatılacağını söylüyor

---

## 📱 Responsive Tasarım

- Mobil cihazlara uyumlu arayüz
- Dinamik tahta boyutlandırma
- Esnek menü sistemi
- Touch-friendly butonlar

---

## 🔒 Güvenlik

- Flask session yönetimi
- Güvenli form işleme
- XSS koruması
- CSRF koruması

---

## 📬 İletişim

Benimle her zaman iletişime geçebilirsiniz:

[![Web Sitem](https://img.shields.io/badge/Web%20Site-1976d2?style=for-the-badge&logo=google-chrome&logoColor=white)](https://osmandemir2533.github.io/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0a66c2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/osmandemir2533/)

---

> Proje, modern web standartlarına uygun olarak geliştirilmiştir.  
> Hem güvenli hem de kullanıcı dostu bir oyun deneyimi sunar.    

