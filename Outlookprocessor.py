import win32com.client

Outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI") #Opens Microsoft Outlook
''''
for i in range(50):
    print(i)
    try:
        box = outlook.GetDefaultFolder(i)
        name = box.Name
        print(i, name)
    except:
        pass
'''
folder = Outlook.Folders[0] #N4 Invocie folder
subFolder = folder.Folders[0]
subsubfolder = subFolder.Folders[0]
print(f'The subfolder is : {subFolder}')
print(f'The folder is : {subsubfolder}')
folderMessages= subsubfolder.Items
print(folderMessages)
message = folderMessages.GetFirst()
#message = message.GetNext()
print(message.content)
'''
subFolder = folder.Folders[5] #N4 Invoice subfolder
subFolderMessages = subFolder.Items #Invoice items object
message = subFolderMessages.GetFirst()

while True:
subFolderItemAttachments = message.Attachments
nbrOfAttachmentInMessage = subFolderItemAttachments.Count
x = 1
while x <= nbrOfAttachmentInMessage: attachment = subFolderItemAttachments.item(x) #Saves attachment to location attachment.SaveAsFile('C:\\Users\\kkim\\Desktop\\InvoiceOutlook' + '\\'+ str(attachment)) break message = subFolderMessages.GetNext(
'''
