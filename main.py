import cv2
import numpy as np
import tkinter as tk
import settings
from PIL import Image, ImageTk #python image library / görüntü düzenleme
import imutils #imutils real-time videolarda birden çok görüntüyü izleyebilmektedir.
from tkinter import messagebox
import random




def show_frame():
    if not settings.start_video:
        return None

    #sonraki video karesini yakalar, kodunu çözer ve döndürür.Hiçbir çerçeve yakalanmamışsa, görüntü boş olacaktır.
    _, frame = cap.read()
    #frame = cv2.flip(frame, 1)
    frame = imutils.resize(frame, width=600)

    if settings.start_processing:
        frame = process_frame(frame)

    #bir görüntüyü bir renk uzayından diğerine dönüştürür.
    #OpenCV'deki varsayılan renk formatı genellikle RGB olarak adlandırılır, ancak aslında BGR'dir
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #tam sayı veya kayan bir sayısal diziyi görüntüye dönüştürür.
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    #main label dönüşümleri (videoyu başlat'a basın.)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


#algılanan nesne sınıfları
CLASSES = ["arkafon", "ucak", "bisiklet", "kus", "tekne",
        "sise", "otobüs", "araba", "kedi", "sandalye", "inek", "yemekmasasi",
        "kopek", "at", "motorsiklet", "insan", "saksi", "koyun",
        "kanepe", "tren", "tvmonitor"]

#tespit edilen nesne sınıflarının çerçeve renklerini random olarak belirler.
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

#video ekranını arayüzde gösterir.
def start_video():
    settings.start_video = True
    show_frame()

#video ekranı kaybolur ayrıca taramayı da durdurur.
def stop_video():
    settings.start_video = False
    settings.start_processing = False
    lmain.config(image='')


label = None
def process_frame(img):
    global label
    # Çerçeve boyutlarını yakalayıp bir bloba dönüştürür.
    (h, w) = img.shape[:2]
    #resim, ölçeklendirme, boyut,doğruluk
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)),
                                0.007843, (300, 300), 127.5)

    
    # Blob tespit ve tahminlerini alır.
    net.setInput(blob)
    detections = net.forward()

    # Tespit etme döngüsü.
    for i in np.arange(0, detections.shape[2]):
        # Tahmin ile ilgili olasılığı çıkarmak.
        confidence = detections[0, 0, i, 2]

        # Algının zayıf olduğu yerleri için koşul durumu.
        # Minimum güven olasılığından daha büyük.
        if confidence > 0.2:
            # Algılanan kısınmdan sınıf etiketinin dizinini çıkarır,
            # ardından nesne için sınırlayıcı kutunun (x, y) koordinatlarını hesaplar.
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Tahmin olasılığını çerçeveye yazdırır.
            label = "{}: {:.2f}%".format(CLASSES[idx],
                                         confidence * 100)
            # print(label)
            #dikdörtgen çizer.köşe noktaları,rengi,kalınlığı.
            cv2.rectangle(img, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            #metin dizesini yazar.görüntü,yazılacak metin dizesi,konumu,yazı tipi/ölçeği,rengi ve kalınlığı.
            if settings.true_false == True:
                cv2.putText(img, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            else:
                break
                        
    return img


def start_process():
    settings.start_processing = True


def stop_process():
    settings.start_processing = False
    settings.true_false = False


def clickBtn():
    settings.true_false = True
    
    message = label.split(':', 2)

    
    if message[0] == "tvmonitor":
        messagebox.showinfo("Tvmonitor","Görüntü sergilemek için kullanılan elektronik ya da elektro-mekanik aygıtların genel adıdır. Başta televizyon ve bilgisayar olmak üzere birçok elektronik cihazın en önemli çıktı aygıtıdır.")
    elif message[0] == "ucak":
        messagebox.showinfo("Uçak","Hava akımının başta kanatlar olmak üzere kanat profilli parçaların alt ve üst yüzeyleri arasında basınç farkı oluşturması sayesinde havada tutunarak yükselebilen, ilerleyebilen motorlu bir hava taşıtıdır.")
    elif message[0] == "bisiklet":
        messagebox.showinfo("Bisiklet","Motorsuz olan, iki tekerleği bulunan, pedallı, insan gücü ile ilerlemeye yarayan bir ulaşım aracıdır. Spor yapmak için de kullanılır.")
    elif message[0] == "kus":
        messagebox.showinfo("Kuş","Akciğerli, sıcakkanlı, bedeni tüylerle örtülü, gagalı, iki ayaklı ve iki kanatlı, yumurtlayan omurgalı hayvandır. Çeneler, gagayı oluşturan boynuzsu bir kılıfla kaplanmıştır.")
    elif message[0] == "tekne":
        messagebox.showinfo("Gemi","Su üstünde dengede durabilen, manevra kabiliyeti bulunan (makine, yelken, kürek yardımı vb.) belli bir büyüklüğe sahip olan ulaşım aracıdır.")
    elif message[0] == "sise":
        messagebox.showinfo("Şişe","Ağzı gövdesinden daha dar olan, genellikle plastik, alüminyum veya camdan imal edilen taşıyıcı kaptır. Şişeler daha çok, sıvı maddeleri taşımak veya saklamak için kullanılır.")
    elif message[0] == "otobüs":
        messagebox.showinfo("Otobüs","Sürücü dahil 17 kişiden fazla yolcu kapasitesi olan motorlu kara taşıtıdır.")
    elif message[0] == "araba":
        messagebox.showinfo("Araba","Yolcu ve yük taşımaya uygun tekerlekli, motorlu veya motorsuz hareket edebilen her türlü kara ulaşım taşıtı. Motorsuz olanlar hayvanlarla ya da insanlar tarafından yürütülür.")
    elif message[0] == "kedi":
        messagebox.showinfo("Kedi","Küçük, genelde tüylü, evcilleştirilmiş, etobur memeli. Genelde ev hayvanı olarak beslenenlere ev kedisi, ya da diğer kedigillerden ve küçük kedilerden ayırmak gerekmiyorsa kısaca kedi denir. İnsanlar kedilerin arkadaşlığına ve haşarat ev zararlılarını avlayabilme yeteneğine önem vermektedir.")
    elif message[0] == "sandalye":
        messagebox.showinfo("Sandalye","Oturmak için kullanılan bir eşyadır. Genellikle bir kişinin oturabileceği ebatta olup, çeşitli şekillerde ve malzemelerle imal edilebilmektedir. Asıl olarak dört ayağı, oturma kısmı ve sırt bölümü bulunmaktadır.")
    elif message[0] == "inek":
        messagebox.showinfo("İnek","Çoğunlukla evcil olan, kaba ve hantal yapılı, kuyrukları püsküllü, boynuzlu büyükbaş hayvanlardır. Mideleri dört gözlüdür ve geviş getirirler. Üst çenelerinde kesici dişleri bulunmaz. Otları alt çenelerinin dişleriyle keserler.")
    elif message[0] == "yemekmasasi":
        messagebox.showinfo("Yemek masası","Ayaklar veya bir destek üzerine oturtulmuş tabladan oluşan bir mobilyadır. En yaygın masa türü, dört ayak üzerine yerleştirilmiş, dikdörtgen ahşap bir yüzeyden oluşanıdır. Yemek yemek, çalışmak gibi bireysel amaçların yanı sıra, farklı kişileri toplamak, eşyaları belli bir yükseklikte tutmak gibi amaçlar için de kullanılır.")
    elif message[0] == "kopek":
        messagebox.showinfo("Köpek","Küçük, orta ve büyük ırklar olduğu ve her biri bir amaç için insanlar tarafından seçilip evcilleştirildiği için çok değişken bir boyuta sahip bir memelidir. Çok yönlü bir hayvandır ve fizyolojik olarak çok benzersiz bir özelliğe sahiptir")
    elif message[0] == "at":
        messagebox.showinfo("At","Tek tırnaklılar takımının, Atgiller familyasından bir memelidir. Erkeğine aygır, dişisine kısrak, yavrusuna tay denir. Küçük başlı ve kısa kulaklıdır. Yelesi ve kuyruk ucu uzun kıllıdır.")
    elif message[0] == "motorsiklet":
        messagebox.showinfo("Motosiklet","İki ya da üç tekerlekli, bisiklet benzeri, içten yanmalı motora sahip bir ya da iki kişilik ulaşım aracıdır.")
    elif message[0] == "saksi":
        messagebox.showinfo("Saksı","Çiçek ve diğer bitkilerin yetiştirildiği ve sergilendiği bir konteyner. Saksı günümüzde plastik, tahta, taş, bazen dönüşümlü malzemeden de üretilebilmektedir. Alt kısmında fazla suyun akması için delikler bulunur ve tabak şeklinde bir altlığı vardır, bu altlık deliklerden akan suyun dışarı taşmasını engeller.")
    elif message[0] == "koyun":
        messagebox.showinfo("Koyun","Keçiler ile birlikte 'Caprinae' alt familyası içerisinde yer alan bir memeli cinsi. Cinsin coğrafi olarak ve nüfusça en yaygın türü Evcil koyun olmaktadır, ancak pek çok yabani tür de 'Ovis' cinsine aittir.")
    elif message[0] == "kanepe":
        messagebox.showinfo("Kanepe","En az iki ya da daha çok kişinin oturabileceği büyüklükte, kumaş kaplı, içinde ya da üstünde şilte yastıklar bulunan, sırt dayamak için arkalığı ve kolları olan mobilya.")
    elif message[0] == "tren":
        messagebox.showinfo("Tren","Raylar üzerinde bir ya da birkaç lokomotif tarafından çekilen veya itilen vagonlardan oluşan ulaşım aracı.")
    else:
        messagebox.showinfo("Arkaplan","Herhangi bir eylemde daha geri planda yer alan ve asıl eylemin kendisi olmadığı herhangi bir şeyi açıklamak için kullanılan sözcüktür. Bilgisayarlarımızda, yazılımlarımızda ve hatta web sitelerimizde arka plan resmi kullandığımızda asıl amacın dışına çıkmamış oluruz.")
    


def isEqual1():
    message = label.split(':', 2)
    text1 = randomBtn1.cget('text')

    if text1 == message[0]:
        return clickBtn()
    else:
        messagebox.showinfo("Yanlış","Seçtiğiniz şık yanlıştır!")

def isEqual2():
    message = label.split(':', 2)
    text2 = randomBtn2.cget('text')

    if text2 == message[0]:
        return clickBtn()
    else:
        messagebox.showinfo("Yanlış","Seçtiğiniz şık yanlıştır!")

def isEqual3():
    message = label.split(':', 2)
    text3 = randomBtn3.cget('text')

    if text3 == message[0]:
        return clickBtn()
    else:
        messagebox.showinfo("Yanlış","Seçtiğiniz şık yanlıştır!")

def refresh():
    randomBtn1['text'] = random.choice(CLASSES)
    randomBtn2['text'] = random.choice(CLASSES)
    randomBtn3['text'] = random.choice(CLASSES)
    i = 1
    while i < 100:
        if (randomBtn1['text'] == randomBtn2['text'] ) or (randomBtn1['text'] == randomBtn3['text'] ):
            randomBtn1['text'] = random.choice(CLASSES)
            i += 1
        elif (randomBtn2['text'] == randomBtn1['text'] ) or (randomBtn2['text'] == randomBtn3['text'] ):
            randomBtn2['text'] = random.choice(CLASSES)
            i += 1
        elif (randomBtn3['text'] == randomBtn1['text'] ) or (randomBtn3['text'] == randomBtn2['text'] ):
            random1 = random.choice(CLASSES)
            i += 1
        else:
            break
    

# Modelleri disk dosyalarından okuma.
print("Model Yükleniyor...")
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')
cap = cv2.VideoCapture(1)

window = tk.Tk()
window.title("Uygulama Penceresi")
window.config(bg = "sky blue")
window.geometry("870x650")

lbl = tk.Label(window, text="Nesne Tanıma Ekranı", font=("Arial Bold", 24))
lbl.config(bg = "sky blue")
lbl.grid(column=2, row=0)

imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(column=2, row=1 , padx=10, pady=2)


lmain = tk.Label(imageFrame, text="Videoyu başlat'a basın", font = ("Arial Bold", 14))
lmain.config(bg = "sky blue")
lmain.grid(column=2, row=1)

startVideoStreamBtn = tk.Button(window, text="Videoyu başlat", command=start_video)
startVideoStreamBtn.config(bg = "snow2")
startVideoStreamBtn.grid(column=1, row=2, padx=15, pady=5)


stopVideoStreamBtn = tk.Button(window, text="Videoyu durdur", command=stop_video)
stopVideoStreamBtn.config(bg = "snow2")
stopVideoStreamBtn.grid(column=1, row=3, padx=15, pady=5)


startProcessBtn = tk.Button(window, text="Taramayı başlat", command=start_process)
startProcessBtn.config(bg = "snow2")
startProcessBtn.grid(column=3, row=2, padx=15, pady=5)

stopProcessBtn = tk.Button(window, text="Taramayı durdur", command=stop_process)
stopProcessBtn.config(bg = "snow2")
stopProcessBtn.grid(column=3, row=3, padx=15, pady=5)

descriptionBtn = tk.Button(window, text="Şeçenekleri Yenile", command=refresh)
descriptionBtn.config(bg = "snow2")
descriptionBtn.grid(column = 2, row = 2, padx = 15, pady=5)

randomBtn1 = tk.Button(window, command=isEqual1)
randomBtn1.config(bg = "snow2")
randomBtn1.grid(column = 2, row = 3, padx = 15, pady=5)

randomBtn2 = tk.Button(window, command=isEqual2)
randomBtn2.config(bg = "snow2")
randomBtn2.grid(column = 2, row = 4, padx = 15, pady=5)

randomBtn3 = tk.Button(window, command=isEqual3)
randomBtn3.config(bg = "snow2")
randomBtn3.grid(column = 2, row = 5, padx = 15, pady=5)


window.mainloop()
