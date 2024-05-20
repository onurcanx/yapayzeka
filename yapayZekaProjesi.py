import tkinter as tk
from tkinter import messagebox
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Eğitilmiş SVM modeli
svm_model = None
# Veri ön işleme scaler
scaler = None
# Veri kümesi
X = None

def train_model():
    global svm_model, scaler, X
    
        # Veri kümesini yükle
    veri_kumesi = pd.read_excel("C:/Users/goktu/Downloads/diabetes.xlsx")

    # "Outcome" sütununu düşürerek X ve y'yi ayır
    global X
    X = veri_kumesi.drop("Outcome", axis=1)
    y = veri_kumesi["Outcome"]

    # Verileri eğitim ve test setlerine böle
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Verileri standartlaştır
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    lr = LinearRegression()
    lr.fit(X_train,y_train)
    tahminn = lr.predict(X_test)
    #print(tahminn)
    # SVM modelini eğit
    svm_model = SVC(kernel='linear', random_state=0)
    svm_model.fit(X_train_scaled, y_train)

    # Doğruluk oranını hesapla ve ekrana yazdır
    train_accuracy = svm_model.score(X_train_scaled, y_train)
    test_accuracy = svm_model.score(X_test_scaled, y_test)
    print("Test Seti Doğruluk Oranı:", test_accuracy)

    predictions = svm_model.predict(X_test_scaled)

    # Grafik oluştur
    plt.figure(figsize=(10, 5))
    plt.plot(predictions, label='Tahmin Edilen Sonuçlar', color='blue')
    plt.plot(y_test.values, label='Gerçek Sonuçlar', color='red')
    plt.title('Tahmin Edilen Sonuçlar ve Gerçek Sonuçlar')
    plt.xlabel('Veri Örneği')
    plt.ylabel('Sonuç')
    plt.legend()
    plt.show()

def predict_diabetes():
    global svm_model, scaler, X
    
    # Eğer model veya scaler tanımlı değilse, eğitimi yap
    if svm_model is None or scaler is None:
        train_model()
    
    # Kullanıcının girdiği değerleri al
    pregnancies = float(pregnancies_entry.get())
    glucose = float(glucose_entry.get())
    blood_pressure = float(blood_pressure_entry.get())
    skin_thickness = float(skin_thickness_entry.get())
    insulin = float(insulin_entry.get())
    bmi = float(bmi_entry.get())
    diabetes_pedigree = float(diabetes_pedigree_entry.get())
    age = float(age_entry.get())
    
    # Girdileri bir veri çerçevesine dönüştür
    user_data = pd.DataFrame([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]], columns=X.columns)
    
    # Verileri standartlaştır
    user_data_scaled = scaler.transform(user_data)
    
    # Model tarafından tahmin yap
    prediction = svm_model.predict(user_data_scaled)
    
    # Tahmini kullanıcıya göster
    if prediction[0] == 1:
        result_label.config(text="Diyabet riski var", fg="red")
    else:
        result_label.config(text="Diyabet riski yok", fg="green")   

# Tkinter uygulaması
root = tk.Tk()
root.title("Diyabet Tahmini")

# Etiketler oluştur
pregnancies_label = tk.Label(root, text="Hamilelik Sayısı:")
pregnancies_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
glucose_label = tk.Label(root, text="Glikoz:")
glucose_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
blood_pressure_label = tk.Label(root, text="Kan Basıncı:")
blood_pressure_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
skin_thickness_label = tk.Label(root, text="Cilt Kalınlığı:")
skin_thickness_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
insulin_label = tk.Label(root, text="İnsülin:")
insulin_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
bmi_label = tk.Label(root, text="Vücut Kitle İndeksi (BMI):")
bmi_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
diabetes_pedigree_label = tk.Label(root, text="Diyabet Soy Ağacı:")
diabetes_pedigree_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
age_label = tk.Label(root, text="Yaş:")
age_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")

# Giriş kutuları oluştur
pregnancies_entry = tk.Entry(root)
pregnancies_entry.grid(row=0, column=1, padx=10, pady=5)
glucose_entry = tk.Entry(root)
glucose_entry.grid(row=1, column=1, padx=10, pady=5)
blood_pressure_entry = tk.Entry(root)
blood_pressure_entry.grid(row=2, column=1, padx=10, pady=5)
skin_thickness_entry = tk.Entry(root)
skin_thickness_entry.grid(row=3, column=1, padx=10, pady=5)
insulin_entry = tk.Entry(root)
insulin_entry.grid(row=4, column=1, padx=10, pady=5)
bmi_entry = tk.Entry(root)
bmi_entry.grid(row=5, column=1, padx=10, pady=5)
diabetes_pedigree_entry = tk.Entry(root)
diabetes_pedigree_entry.grid(row=6, column=1, padx=10, pady=5)
age_entry = tk.Entry(root)
age_entry.grid(row=7, column=1, padx=10, pady=5)

# Sonuç etiketi
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.grid(row=8, columnspan=2, padx=10, pady=10)

# Tahmin düğmesi
predict_button = tk.Button(root, text="Diyabeti Tahmin Et", command=predict_diabetes)
predict_button.grid(row=9, columnspan=2, padx=10, pady=10)


root.mainloop()
train_model()
