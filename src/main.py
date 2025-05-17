import os
import fnmatch
import requests
import zipfile
import sys
import time

class Main:

  def __init__(self):
    print("MainClass instanziiert")
    
  def processPDFFiles(self):
    print("Programm gestartet")
    url = "http://127.0.0.1:8080/metadata"
    inputDir = "C:/Users/Matthias/Documents/pypdf/01-input/"
    outputDir = "C:/Users/Matthias/Documents/pypdf/03-output/"

    counterDict = {}
    counterDict['AD']  = 1
    counterDict['RF']  = 1
    counterDict['RP']  = 1

    tmpZipPath = ""


    for root, dirs, files in os.walk(inputDir):
      for fileName in fnmatch.filter(files, "*.pdf"):
        print("--------------------------------------------------")
        print(fileName)
        inputFilePath = inputDir + fileName
        print(inputFilePath)

        try:
          with open(inputFilePath, 'rb') as aFile:
            #files = {'file': aFile}
            
            # Add custom headers if needed
            headers = {
                'User-Agent': 'PDF Upload Client/1.0'
            }
            
            response = requests.post(url, files={'file': aFile}, headers=headers)
            
            jsonResponse =response.json()
            print(jsonResponse)
            print(jsonResponse["barcode"])

            if (jsonResponse["barcode"] != "NONE"):
              #barcodeValue = jsonResponse["barcode"][:2]
              barcodeValue = jsonResponse["barcode"]
              counter = str(counterDict[barcodeValue[:2]])
              #print("counter: " + str(counter))
              zipPath = inputDir + counter + "__" + barcodeValue + ".zip"
              tmpZipPath = zipPath
              print("BARCODE found: " + tmpZipPath)
              with zipfile.ZipFile(zipPath, 'w') as zipf:
                zipf.write(inputFilePath, fileName)
              
              counterDict[barcodeValue[:2]] += 1
            
            percentageWhitePixels = float(jsonResponse["percentageWhitePixels"])

            if (jsonResponse["barcode"] == "NONE" and percentageWhitePixels < 0.99):
              print("NONE: " + tmpZipPath)
              with zipfile.ZipFile(tmpZipPath, 'a') as zipf:
                zipf.write(inputFilePath, fileName)
         
        except FileNotFoundError:
          print(f"Error: File not found at {inputFilePath}")

        except Exception as e:
          print(f"An error occurred: {str(e)}")


  def processMergeAndConvert(self):

    url = "http://127.0.0.1:8080/mergepdf"
    inputDir = "C:/Users/Matthias/Documents/pypdf/01-input/"
    outputDir = "C:/Users/Matthias/Documents/pypdf/03-output/"
    mergedPFD = []
    
    for root, dirs, files in os.walk(inputDir):
      for fileName in fnmatch.filter(files, "*.zip"): 
        try:
          inputFilePath = inputDir + fileName
          print(inputFilePath)
          with open(inputFilePath, 'rb') as aFile:
          #files = {'file': aFile}
            
          # Add custom headers if needed
            headers = {
              'User-Agent': 'PDF Upload Client/1.0'
            }
     
            outputFilePath = inputFilePath[:-4]  + ".pdf"
            print(outputFilePath)
            response = requests.post(url, files={'file': aFile}, headers=headers)
            file = open(outputFilePath, "wb")
            file.write(response.content)
            file.flush()
            file.close()
            mergedPFD.append(outputFilePath)
            #time.sleep(14)
            #sys.exit()
          
        except FileNotFoundError:
          print(f"Error: File not found at {inputFilePath}")

        except Exception as e:
          print(f"An error occurred: {str(e)}")

    print(mergedPFD)

    for pdfFile in mergedPFD:
        url = "http://127.0.0.1:8080/convertpdfa"
        try:
          #inputFilePath = outputFilePath
          print(pdfFile)
          with open(pdfFile, 'rb') as aFile:
          #files = {'file': aFile}
            
          # Add custom headers if needed
            headers = {
              'User-Agent': 'PDF Upload Client/1.0'
            }
     
            outputFilePath = pdfFile[:-4]  + "_pdfa-1b.pdf"
            print(outputFilePath)
            response = requests.post(url, files={'file': aFile}, headers=headers)
            file = open(outputFilePath, "wb")
            file.write(response.content)
            file.flush()
            file.close()
            #time.sleep(5)
            #sys.exit()
          
        except FileNotFoundError:
          print(f"Error: File not found at {inputFilePath}")

        except Exception as e:
          print(f"An error occurred: {str(e)}")

        
      




if __name__ == "__main__":
 app = Main()  # Instanz der Main-Klasse erstellen
 app.processPDFFiles()
 app.processMergeAndConvert()




