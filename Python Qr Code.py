import os
import wx
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import ImageOps
try:
    import qrcode
except ImportError:
    qrcode = None
 
try:
    import PyQRNative
except ImportError:
    PyQRNative = None
 
########################################################################
class QRPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.photo_max_size = 300
        sp = wx.StandardPaths.Get()
        self.defaultLocation = sp.GetDocumentsDir()
 
        img = wx.EmptyImage(300,300)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.BitmapFromImage(img))
 
        qrDataLbl = wx.StaticText(self, label="Text to turn into QR Code:")
        self.qrDataTxt = wx.TextCtrl(self, value="", size=(200,-1))
        qrTextLbl = wx.StaticText(self, label="QR Code Image Text:")
        self.qrTextTxt = wx.TextCtrl(self, value="", size=(200,-1))
       # instructions = "Name QR image file"
        #instructLbl = wx.StaticText(self, label=instructions)
        #self.qrPhotoTxt = wx.TextCtrl(self, size=(200,-1))
        browseBtn = wx.Button(self, label='Change Save Location')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        defLbl = "Default save location: " + self.defaultLocation
        self.defaultLocationLbl = wx.StaticText(self, label=defLbl)
 
        qrcodeBtn = wx.Button(self, label="Create QR with qrcode")
        qrcodeBtn.Bind(wx.EVT_BUTTON, self.onUseQrcode)
     
 
        # Create sizer
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        qrDataSizer = wx.BoxSizer(wx.HORIZONTAL)
        qrTextSizer = wx.BoxSizer(wx.HORIZONTAL)
        locationSizer = wx.BoxSizer(wx.HORIZONTAL)
        qrBtnSizer = wx.BoxSizer(wx.VERTICAL)
 
        qrDataSizer.Add(qrDataLbl, 0, wx.ALL, 5)
        qrDataSizer.Add(self.qrDataTxt, 1, wx.ALL|wx.EXPAND, 5)
		
        qrTextSizer.Add(qrTextLbl, 0, wx.ALL, 5)
        qrTextSizer.Add(self.qrTextTxt, 1, wx.ALL|wx.EXPAND, 5)

        qrBtnSizer.Add(qrcodeBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(wx.StaticLine(self, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(qrDataSizer, 0, wx.EXPAND)
        self.mainSizer.Add(qrTextSizer, 0, wx.EXPAND)
        self.mainSizer.Add(qrBtnSizer, 0, wx.ALL|wx.CENTER, 10)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        #locationSizer.Add(instructLbl, 0, wx.ALL, 5)
        #locationSizer.Add(self.qrPhotoTxt, 0, wx.ALL, 5)
        self.mainSizer.Add(self.defaultLocationLbl, 0, wx.ALL, 5)
        locationSizer.Add(browseBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(locationSizer, 0, wx.ALL, 5)
 
       
 
        self.SetSizer(self.mainSizer)
        self.Layout()
 
    #----------------------------------------------------------------------
    def onBrowse(self, event):
        """"""
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.defaultLocation = path
            self.defaultLocationLbl.SetLabel("Save location: %s" % path)
        dlg.Destroy()
 
    #----------------------------------------------------------------------
    def onUseQrcode(self, event):
        """

https://github.com/lincolnloop/python-qrcode

        """
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=20, border=4)
        qr.add_data(self.qrDataTxt.GetValue())
        qr.make(fit=True)
        x = qr.make_image()
        x = ImageOps.expand(x,border=20,fill='white')
        x = ImageOps.expand(x,border=10,fill=0)
        width, height = x.size
        draw = ImageDraw.Draw(x)
        font = ImageFont.truetype("WhiteRabbit.ttf", 50)
        text = self.qrTextTxt.GetValue()
        text_x, text_y = font.getsize(text)
        xt = (width - text_x)/2
        yt = (height - text_y)/2
        draw.text((xt, 20),text,fill=0,font=font)
		
        qr_file = os.path.join(self.defaultLocation, self.qrDataTxt.GetValue() + ".png")
        img_file = open(qr_file, 'wb')
        x.save(img_file, 'PNG')
        img_file.close()
        
        blank_image = Image.new("RGB", (int(width*2+10), height), 0)
        blank_image.paste(x, (0,0))
        blank_image.paste(x, (int(width*2+10)-width,0))
        qr_fileD = os.path.join(self.defaultLocation, self.qrDataTxt.GetValue() + " Print.png")
        img_fileD = open(qr_fileD, 'wb')
        blank_image.save(img_fileD, 'PNG')
        img_file.close()
        
        self.showQRCode(qr_file)
 
    #----------------------------------------------------------------------
   
    def showQRCode(self, filepath):
        """"""
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.photo_max_size
            NewH = self.photo_max_size * H / W
        else:
            NewH = self.photo_max_size
            NewW = self.photo_max_size * W / H
        img = img.Scale(NewW,NewH)
 
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.Refresh()
 
 
########################################################################
class QRFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="QR Code Viewer", size=(650,700))
        panel = QRPanel(self)
 
if __name__ == "__main__":
    app = wx.App(False)
    frame = QRFrame()
    frame.Show()
    app.MainLoop()