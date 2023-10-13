import os
# import fitz
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image
from PyQt6.QtWidgets import QMessageBox

class PDF():
    def constructor(self, _from, _to, _page, _cpu_mode, _l_ident_act, _l_fname_act, _l_kycdt_act):
        self.source = _from.text()
        self.savein = _to.text()
        self.npages = _page
        self.get_cpu_mode = _cpu_mode.isChecked()
        self.get_l_ident_act = _l_ident_act.isChecked()
        self.get_l_fname_act = _l_fname_act.isChecked()
        self.get_l_kycdt_act = _l_kycdt_act.isChecked()

    def pdf_from_img(self):
        self.tree = os.listdir(self.source)
        for leaf in self.tree:
            current_file_name = f'{self.source}{leaf}'
            upper_file_name = current_file_name.upper().replace('.PDF','.pdf').replace('.PNG','.png').replace('.JPG','.jpg').replace('.JPEG','.jpeg').replace('.JFIF','.jfif')
            try: os.rename(current_file_name,upper_file_name)
            except: pass
        self.tree = os.listdir(self.source)
        for leaf in self.tree:
            if not leaf.__contains__('.pdf') and not leaf.__contains__('AFF'):
                try:
                    _img = Image.open(f'{self.source}{leaf}')
                    _img = _img.convert('RGB')
                    new_pdf = f'{self.source}{leaf}'
                    new_pdf = new_pdf.replace('.png','.pdf').replace('.jpg','.pdf').replace('.jpeg','.pdf').replace('.jfif','.pdf')
                    _img.save(new_pdf)
                except Exception as e: pass
                try: os.remove(f'{self.source}{leaf}')
                except Exception as e: pass

    def pdf_merge(self):
        self.tree = os.listdir(self.source)
        self.count = 0
        self._merge = PdfMerger()
        self._remove = []
        self.output_name = f'{self.source}ID'
        if self.get_l_ident_act: self.output_name += f' {self.l_ident.text()}'
        if self.get_l_fname_act: self.output_name += f' {self.l_fname.text()}'
        if self.get_l_kycdt_act: self.output_name += f' {self.l_kycdt.text()}'
        self.output_name += '.pdf'
        for leaf in self.tree:
            if leaf.__contains__('ID1.pdf') or leaf.__contains__('ID2.pdf'):
                self._merge.append(f'{self.source}{leaf}')
                self._remove.append(f'{self.source}{leaf}')
                self.count += 1
        if self.count == 2:
            with open(self.output_name, 'wb') as f:
                self._merge.write(f)
                self._merge.close()
                f.close()
            for r in self._remove:
                try: os.remove(r)
                except Exception as e: pass

    def pdf_text(self):
        self.tree = os.listdir(self.source)
        self.searchx = f'{self.source}{self.tree[0]}'
        self.is_doc_kyc = [False, [], []]
        self.is_doc_cic = [False, [], []]
        self.is_doc_ccac = [False, []]
        self.is_doc_decl = [False, []]
        self.is_doc_cons = [False, []]
        self.is_doc_cert = [False, []]
        self._pdf = open(self.searchx, 'rb')
        self._reader = PdfReader(self._pdf)
        self._pages = self._reader.pages
        _len = self._pages.__len__()
        for n in range(_len):
            self.raw_text = self._pages[n].extract_text().replace('\n',' ')
            self.kyc_rawtext = self._pages[n].extract_text().replace('\xa0','').split('\n')
            self.cic_rawtext = self._pages[n].extract_text().replace('\xa0','').split('\n')
            self.raw_text = self.raw_text.lower()
            if self.raw_text.__contains__('ley') and self.raw_text.__contains__('8204') and self.raw_text.__contains__('regulaciones') and self.raw_text.__contains__('conozca') and self.raw_text.__contains__('cliente') and self.raw_text.__contains__('agradecemos') and self.raw_text.__contains__('confidencialidad') and self.raw_text.__contains__('civil') and self.raw_text.__contains__('actividad') and self.raw_text.__contains__('laboral') and self.raw_text.__contains__('perfil') and self.raw_text.__contains__('transaccional'):
                self.is_doc_kyc[0] = True # kyc pág. 1
                self.is_doc_kyc[1].append(n)
                for rt in self.kyc_rawtext:
                    _rt = rt.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
                    if _rt.__contains__('fecha') and _rt.__contains__('codigo'):
                        raw_line = _rt
                        raw_line = raw_line.replace('\xa0','').replace('codigo','').replace('fecha','')
                        raw_line = raw_line.split(' ')
                        raw_line.pop()
                        raw_line.pop()
                        raw_line.pop()
                        month = raw_line[-2].upper().split(' ')
                        month = month[0]
                        if month == 'ENERO': month = '01'
                        elif month == 'FEBRERO': month = '02'
                        elif month == 'MARZO': month = '03'
                        elif month == 'ABRIL': month = '04'
                        elif month == 'MAYO': month = '05'
                        elif month == 'JUNIO': month = '06'
                        elif month == 'JULIO': month = '07'
                        elif month == 'AGOSTO': month = '08'
                        elif month == 'SEPTIEMBRE': month = '09'
                        elif month == 'OCTUBRE': month = '10'
                        elif month == 'NOVIEMBRE': month = '11'
                        elif month == 'DICIEMBRE': month = '12'
                        raw_line = f'{month}-{raw_line[-1]}'
                        self.is_doc_kyc[2].append(raw_line)
                    elif _rt.__contains__('primer nombre') and _rt.__contains__('segundo nombre'):
                        _rt = _rt.replace('primer','').replace('segundo','').replace('nombre','').replace('apellido','')
                        _rt = _rt.split(' ')
                        raw_line = []
                        for item in _rt:
                            if item != '': raw_line.append(item)
                        raw_line = ' '.join(raw_line)
                        raw_line = raw_line.split(' ')
                        if len(raw_line) == 2: raw_line = raw_line.reverse()
                        elif len(raw_line) == 3: raw_line = f'{raw_line[-2]} {raw_line[-1]} {raw_line[0]}'
                        elif len(raw_line) == 4: raw_line = f'{raw_line[-2]} {raw_line[-1]} {raw_line[0]} {raw_line[1]}'
                        elif len(raw_line) > 4:
                            lastname = f'{raw_line[-2]} {raw_line[-1]}'
                            raw_line.pop()
                            raw_line.pop()
                            raw_line = ' '.join(raw_line)
                            raw_line = f'{lastname} {raw_line}'
                        self.is_doc_kyc[2].append(raw_line.upper())
                    elif _rt.__contains__('numero') and _rt.__contains__('identificacion') and _rt.__contains__('tipo') and _rt.__contains__('estado'):
                        raw_line = ''
                        for char in _rt:
                            x = char.isnumeric()
                            if x: raw_line += char
                        self.is_doc_kyc[2].append(raw_line)
                self.is_doc_kyc[2].reverse()
            elif self.raw_text.__contains__('cumple') and self.raw_text.__contains__('cumplido') and self.raw_text.__contains__('territorio') and self.raw_text.__contains__('(pep)') and self.raw_text.__contains__('expuesta') and self.raw_text.__contains__('juramento') and self.raw_text.__contains__('testimonio') and self.raw_text.__contains__('autorizo') and self.raw_text.__contains__('adicional') and self.raw_text.__contains__('requiera') and self.raw_text.__contains__('solicitud') and self.raw_text.__contains__('comprometo'):
                self.is_doc_kyc[0] = True # kyc pág. 2
                self.is_doc_kyc[1].append(n)
            elif self.raw_text.__contains__('autorizac') and self.raw_text.__contains__('persona') and self.raw_text.__contains__('informac') and self.raw_text.__contains__('crediticia') and self.raw_text.__contains__('entidad') and self.raw_text.__contains__('supervisada'):
                self.is_doc_cic[0] = True # cic
                for rt in self.kyc_rawtext:
                    _rt = rt.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
                    if _rt.__contains__('yo,') and _rt.__contains__('identificacion') and _rt.__contains__('autorizo'):
                        raw_line = _rt
                        break
                raw_line = raw_line.split(',')
                raw_line[2] = raw_line[2].replace('identificacion','').replace('numero','')
                raw_line = f'{raw_line[1].upper()} {raw_line[2]}'
                raw_line = raw_line.split(' ')
                striped_rawline = []
                for rl in raw_line:
                    if rl != '': striped_rawline.append(rl)
                raw_line = ''
                self.is_doc_cic[2].append(striped_rawline.pop())
                raw_line = striped_rawline
                if len(raw_line) == 2: raw_line = raw_line.reverse()
                elif len(raw_line) == 3: raw_line = f'{raw_line[-2]} {raw_line[-1]} {raw_line[0]}'
                elif len(raw_line) == 4: raw_line = f'{raw_line[-2]} {raw_line[-1]} {raw_line[0]} {raw_line[1]}'
                elif len(raw_line) > 4:
                    lastname = f'{raw_line[-2]} {raw_line[-1]}'
                    raw_line.pop()
                    raw_line.pop()
                    raw_line = ' '.join(raw_line)
                    raw_line = f'{lastname} {raw_line}'
                self.is_doc_cic[2].append(raw_line)
                self.is_doc_cic[1].append(n)
            elif self.raw_text.__contains__('expediente') and self.raw_text.__contains__('otorgo') and self.raw_text.__contains__('mediante') and self.raw_text.__contains__('firma') and self.raw_text.__contains__('multimoney') and self.raw_text.__contains__('cicac') and self.raw_text.__contains__('acceso') and self.raw_text.__contains__('transfiera') and self.raw_text.__contains__('siempre') and self.raw_text.__contains__('verificar'):
                self.is_doc_ccac[0] = True # cicac
                self.is_doc_ccac[1].append(n)
            elif self.raw_text.__contains__('jurada') and self.raw_text.__contains__('mayor') and self.raw_text.__contains__('identidad') and self.raw_text.__contains__('manifiesto') and self.raw_text.__contains__('declaro') and self.raw_text.__contains__('juramento') and self.raw_text.__contains__('negociados') and self.raw_text.__contains__('central') and self.raw_text.__contains__('sugef') and self.raw_text.__contains__('respetando') and self.raw_text.__contains__('trabajo') and self.raw_text.__contains__('ciudad'):
                self.is_doc_decl[0] = True # affidavit
                self.is_doc_decl[1].append(n)
            elif self.raw_text.__contains__('consentimiento') and self.raw_text.__contains__('informado') and self.raw_text.__contains__('debidamente') and self.raw_text.__contains__('sociedad') and self.raw_text.__contains__('siguiente') and self.raw_text.__contains__('custodia') and self.raw_text.__contains__('autorizo') and self.raw_text.__contains__('expresamente') and self.raw_text.__contains__('saldo') and self.raw_text.__contains__('actual') and self.raw_text.__contains__('entiendo') and self.raw_text.__contains__('firmamos'):
                self.is_doc_cons[0] = True # authorization
                self.is_doc_cons[1].append(n)
            elif self.raw_text.__contains__('certifica') and self.raw_text.__contains__('sistema') and self.raw_text.__contains__('consta') and self.raw_text.__contains__('evidencia') and self.raw_text.__contains__('generada') and self.raw_text.__contains__('firma') and self.raw_text.__contains__('lectura') and self.raw_text.__contains__('contenido') and self.raw_text.__contains__('mostrado') and self.raw_text.__contains__('firmantes') and self.raw_text.__contains__('integridad') and self.raw_text.__contains__('voluntad.'):
                self.is_doc_cert[0] = True # sign certificate pág. 1/3
                self.is_doc_cert[1].append(n)
            elif self.raw_text.__contains__('firma') and self.raw_text.__contains__('aceptar') and self.raw_text.__contains__('legal') and self.raw_text.__contains__('email') and self.raw_text.__contains__('datos') and self.raw_text.__contains__('identificativos'):
                self.is_doc_cert[0] = True # sign certificate pág. 2/3
                self.is_doc_cert[1].append(n)
            elif self.raw_text.__contains__('detalles') and self.raw_text.__contains__('metros') and self.raw_text.__contains__('otros') and self.raw_text.__contains__('puntos') and self.raw_text.__contains__('para') and self.raw_text.__contains__('verificar') and self.raw_text.__contains__('documento'):
                self.is_doc_cert[0] = True # sign certificate pág. 3/3
                self.is_doc_cert[1].append(n)
        self.is_doc_cert_length = len(self.is_doc_cert[1])
        self._pdf.close()

    def run_wizzard(self):
        self.tree = os.listdir(self.source)
        self._pdf = open(self.searchx, 'rb')
        self._reader = PdfReader(self._pdf)
        self._pages = self._reader.pages
        def of(self):
            if self.get_l_ident_act: self.output_file += f' {self.l_ident.text()}'
            if self.get_l_fname_act: self.output_file += f' {self.l_fname.text()}'
            if self.get_l_kycdt_act: self.output_file += f' {self.l_kycdt.text()}'
            self.output_file += '.pdf'
        for leaf in self.tree:
            if leaf.__contains__('ID.pdf'):
                self.output_file = f'{self.source}ID'
                of(self)
                os.rename(f'{self.source}{leaf}',self.output_file)
        if self.get_cpu_mode:
            if self.is_doc_kyc[0]:
                for l in self.is_doc_cert[1]:
                    self.is_doc_kyc[1].append(l)
                pages = self.is_doc_kyc[1]
                writer = PdfWriter()
                for p in pages:
                    writer.add_page(self._reader.pages[p])
                self.output_file = f'{self.source}KYC'
                of(self)
                with open(self.output_file, 'wb') as f:
                    writer.write(f)
                    f.close()
        if self.is_doc_cic[0]:
            for l in self.is_doc_cert[1]:
                self.is_doc_cic[1].append(l)
            pages = self.is_doc_cic[1]
            writer = PdfWriter()
            for p in pages:
                writer.add_page(self._reader.pages[p])
            self.output_file = f'{self.source}AUTORIZACIÓN CIC'
            of(self)
            with open(self.output_file, 'wb') as f:
                writer.write(f)
                f.close()
        if self.get_cpu_mode:
            if self.is_doc_ccac[0]:
                for l in self.is_doc_cert[1]:
                    self.is_doc_ccac[1].append(l)
                pages = self.is_doc_ccac[1]
                writer = PdfWriter()
                for p in pages:
                    writer.add_page(self._reader.pages[p])
                self.output_file = f'{self.source}AUTORIZACIÓN CICAC'
                of(self)
                with open(self.output_file, 'wb') as f:
                    writer.write(f)
                    f.close()
            if self.is_doc_decl[0]:
                for l in self.is_doc_cert[1]:
                    self.is_doc_decl[1].append(l)
                pages = self.is_doc_decl[1]
                writer = PdfWriter()
                for p in pages:
                    writer.add_page(self._reader.pages[p])
                self.output_file = f'{self.source}DECLARACIÓN JURADA'
                of(self)
                with open(self.output_file, 'wb') as f:
                    writer.write(f)
                    f.close()
            if self.is_doc_cons[0]:
                for l in self.is_doc_cert[1]:
                    self.is_doc_cons[1].append(l)
                pages = self.is_doc_cons[1]
                writer = PdfWriter()
                for p in pages:
                    writer.add_page(self._reader.pages[p])
                self.output_file = f'{self.source}CONSENTIMIENTO INFORMADO'
                of(self)
                with open(self.output_file, 'wb') as f:
                    writer.write(f)
                    f.close()
        self._pdf.close()
        try: os.remove(self.searchx)
        except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)
        self.tree = os.listdir(self.source)

        if self.source != self.savein:
            try: os.rename(self.source,f'{self.savein}/{self.l_ident.text()} {self.l_fname.text()}')
            except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)
        else:
            rename_folder = self.source.split('/')
            rename_folder.pop()
            vsf = rename_folder[-1]
            if vsf.__contains__('Desktop') or vsf.__contains__('Escritorio') or vsf.__contains__('Documents') or vsf.__contains__('Documentos') or vsf.__contains__('Downloads') or vsf.__contains__('Descargas') or vsf.__contains__('Pictures') or vsf.__contains__('Images') or vsf.__contains__('Imágenes'): pass
            else:
                rename_folder.pop()
                rename_folder = '/'.join(rename_folder)
                rename_folder = f'{rename_folder}/{self.l_ident.text()}'
                try: os.rename(self.source,f'{rename_folder} {self.l_fname.text()}')
                except Exception as e: QMessageBox.warning(self, 'DeskPy', f'A runtime error has occurred.\nPlease notify us by means of the error code generated.\n\nerr code: {e}\t\t', QMessageBox.StandardButton.Close)

    def TestingTool(self):
        self.is_subfolders = True
        for leaf in self.tree:
            if leaf.__contains__('.pdf') or leaf.__contains__('.png') or leaf.__contains__('.jpg') or leaf.__contains__('.jpeg') or leaf.__contains__('.jfif'): self.is_subfolders = False
            else: self.is_subfolders = True
