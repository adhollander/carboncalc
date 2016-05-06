from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from biomass import biomass_calc
import sqlite3
import json

UrbForDB = "/home/adh/UrbanForests/UrbanForestCC.sqlite"
regionlist = [u'CenFla', u'GulfCo', u'InlEmp', u'InlVal', u'InterW',  u'LoMidW', u'MidWst', u'NMtnPr', u'NoCalC', u'NoEast', u'PacfNW', u'Piedmt', u'SoCalC', u'SWDsrt', u'TpIntW', u'Tropic']
speclist = [u'ACSP2', u'ACNE', u'ACPA', u'ACRU', u'ACWR', u'ACAC2', u'ALJU', u'ALLE', u'ARHE', u'ARCU', u'AVCA', u'BA', u'BAVA', u'BENI', u'BE', u'BIJA', u'BINO', u'BOSP', u'BDL OTHER', u'BDM OTHER', u'BDS OTHER', u'BEL OTHER', u'BEM OTHER', u'BES OTHER', u'BRPA', u'BRSU', u'BUCA', u'CAME', u'CAPU13', u'CASU34', u'CAVI', u'CAPA3', u'CACA', u'CATO', u'CAGL', u'CAIL', u'CAOV2', u'CAOV', u'CA1', u'CAMI36', u'CABI2', u'CAFI', u'CASSI', u'CAEQ', u'CEDE', u'CELA', u'CECA', u'CHHU', u'CHSP', u'CICA', u'CISP', u'CLQU', u'CL6', u'COUV', u'CONU', u'CEL OTHER', u'CEM OTHER', u'CES OTHER', u'COPR', u'COFL', u'COCI', u'CULA', u'CUAN', u'CUAR', u'CUSE', u'CYCI', u'CYRE11', u'DASI', u'DERE', u'POPI', u'DIVI', u'DYDE2', u'CHLU', u'ELDE', u'ENCY', u'ERJA', u'ERCR', u'EU1', u'EUUN2', u'EUTI', u'FE', u'FIBE2', u'FICA', u'FIEL', u'FILY', u'FI1', u'FRCA', u'FRPE', u'GIBI', u'GLTRIN', u'LOGO', u'GRRO', u'HIMO', u'HITI', u'HYLA', u'ILCO2', u'ILSP', u'ILVO', u'JAMI', u'JAIN', u'JUCH', u'JU', u'JUSI', u'KOELFO', u'LAIN', u'LIJA', u'LILU', u'LIOR', u'LIST', u'LITU', u'LICH', u'LIDE2', u'MATE', u'MAGR', u'MAST', u'MAVI', u'MASO', u'MAPU', u'MAIN', u'MEQU', u'MEAZ', u'MYCE', u'MOAL', u'MUPA', u'NEOL', u'NYSY', u'PEL OTHER', u'PEM OTHER', u'PES OTHER', u'PAAC', u'PATO', u'PEAM', u'PEBO', u'PHCA', u'PHDA4', u'PHRE', u'PHRO', u'PHSY', u'PHSP2', u'PHFR', u'PICL', u'PIEC', u'PIEL2', u'PIPA', u'PI2', u'PITA', u'PIFE', u'PLOC', u'THOR', u'PLAC1', u'POMA', u'PONA', u'PODE', u'PRAN', u'PRCA', u'PRPE2', u'PRSE1', u'PR', u'PYCA', u'PYCO', u'QUAC2', u'QUAL', u'QUFA', u'QUGE', u'QULA', u'QULA2', u'QUMI', u'QUNI', u'QUPH', u'QUSH', u'QU', u'QUNU', u'QUVI', u'RAGL', u'RHIN62', u'SAPA', u'SABA', u'SANI4', u'BRAC', u'SCTE', u'SEPU7', u'SIGL', u'SWMA', u'SYRO', u'TACH', u'TAPA', u'TASP', u'TAIN', u'TAAS', u'TADI', u'TACA', u'TH9', u'TIGR3', u'TITI2', u'TRSE6', u'ULAL', u'ULAM', u'ULPA', u'ULPU', u'ULRU', u'ULS', u'ULX', u'UNP', u'UNS', u'UNT', u'VEME', u'VIOD', u'VISP2', u'WAFI', u'WARO', u'WOBI2', u'CULE', u'YU1', u'ACBU', u'ACGI', u'ACRU_O', u'ACSA1', u'ACSA2', u'AEGL', u'CASA', u'CACO', u'SEBI5', u'CABI', u'CHTH', u'CIAU2', u'CLLU', u'COKO', u'CRPH', u'EUCI', u'EUSA', u'FISI', u'FOIN3', u'FRAM', u'GLTR', u'HIMU3', u'HISY', u'ILCA', u'ILMY', u'ILOP', u'ILOP_S', u'ILAT', u'JUNI', u'JUVI', u'KOBI', u'KOPA', u'LA6_M', u'LA6_N', u'LA6_T1', u'LA6_T2', u'LISI', u'MAGR_L', u'MATR', u'PYAN', u'MA2', u'MEGL', u'MORU', u'OSFR', u'PHSE', u'PIPU', u'PICO5', u'PIEL', u'PINI', u'PIST', u'PIVI', u'PICH', u'PLAC_B', u'PLAC', u'POAL', u'PRAM', u'PRCE', u'PRSE2', u'PYCO2', u'PYCA_B', u'QUAC', u'QUCO', u'QUHE', u'QUCI', u'QULA1', u'QUPA', u'QURU', u'QUST', u'QUVE', u'ROPS', u'SAMI8', u'SAPE12', u'SAMA_T', u'SANI', u'SA', u'SAAL', u'THOC', u'TIAM', u'TICO', u'TRFO', u'ULPA_D', u'ULPA_E', u'VIPR', u'VIAG', u'WIFL', u'CULE2', u'YUGL2', u'ZESE', u'ABPR', u'ACBA2', u'ACDE', u'ACLO', u'ACME', u'ACMA', u'ACOB', u'AECA2', u'AECA3', u'AGFL', u'AIAL', u'ALCO2', u'ALGL', u'ALRH', u'ARUN', u'ARMA2', u'ARRO', u'BAFO', u'BEPE', u'BRAC2', u'BRDI9', u'BRPO', u'BRAR', u'BRBR', u'BRED', u'CATW', u'CACI', u'CADE2', u'CACA3', u'CAED', u'CALE', u'CADE', u'CASP', u'CEAT', u'CEAU', u'CEOC', u'CESI4', u'CESI3', u'CEOC3', u'CHLI', u'CHRE', u'CHTA', u'CILI', u'CISI', u'COLA', u'COAU', u'CRPA', u'CRRU', u'DOVI', u'ERDE', u'ERCA', u'EUCA1', u'EUCI2', u'EUCL', u'EUCO3', u'EUCR', u'EUFI81', u'EUGL', u'EUGLCO', u'EUGR', u'EULE2', u'EULE', u'EUMA23', u'EUNI', u'EUPO', u'EURO', u'EURU', u'EUSI', u'EUTE', u'EUTO11', u'EUVI', u'FIMA2', u'FIMINI', u'FROR2', u'FRANR', u'FRUH', u'FRVE', u'FRVEG', u'GEPA', u'HASU', u'HEAR', u'HYFL', u'ILAL', u'JUCA2', u'JURE', u'KOEL', u'LANO', u'LELA12', u'LIOV', u'LIFO', u'LYAS', u'MATI', u'MALA6', u'MAFL80', u'MASY2', u'MABO', u'MELI7', u'OLEU', u'OLEU2', u'CEFL', u'PIAT', u'PIBR2', u'PICA', u'PICO2', u'PIED', u'PIHA', u'PIMU2', u'PIPI2', u'PIRA', u'PIRO', u'PITH', u'PITO2', u'PIPH2', u'PIRH', u'PITO', u'PIUN', u'PIVI5', u'PLRA', u'POGR2', u'PONI', u'POCA2', u'PRCH', u'PRAR', u'PRBL', u'PRCEKV', u'PRDO', u'PRDU', u'PRIL', u'PRLY', u'PSME', u'PTST', u'PUGR', u'PYCA_A', u'PYKA', u'QUAG', u'QUEN', u'QUIL2', u'QUKE', u'QULO', u'QURO', u'QUSU', u'RHIN', u'ROAMI', u'SAALT', u'SAMA', u'SACANE', u'SCMO', u'SCPO', u'SECO9', u'SESE', u'SEGI', u'SOJA', u'STSI', u'SYPA2', u'TAAV', u'TACH3', u'TRCO', u'TRAC', u'UMCA', u'XYCO', u'YUGU', u'ZESE_V', u'ACPL', u'ACPL_CK', u'ACPS_S', u'AC', u'AECA3_B', u'AECA3_S', u'UNKNB', u'CABE', u'CABE_F', u'CE2', u'CESI2', u'UNKNC', u'CRLA80', u'CR', u'CUMA', u'CU', u'DIKA', u'ELAN', u'FASY', u'FRAM_A', u'FRAM_R', u'FRAN_R', u'FREX', u'FREX_H', u'FREX_K', u'FRHO', u'FROX_F', u'FRPE_M', u'FRPE_P', u'FRPE_S', u'FRVE_FW', u'FRVE_G', u'GIBI_AG', u'GIBI_F', u'GL3', u'GLTR_S', u'JUHI', u'JU1', u'KOPA_F', u'MASO_G', u'MA1', u'OSVI', u'PI1', u'PIPA4', u'PISY', u'PIAT4', u'PICH_PS', u'PI23', u'PLAC_C', u'PLOR', u'PO', u'PRAM2', u'PRAV', u'PRSU', u'PYCA_C', u'PYCA_CH', u'PYCA_R', u'PYCA_T', u'PYCA_W', u'PY', u'QUWI', u'RHLA', u'ROPS_PR', u'SOHUCQ', u'SOHUCF', u'TI', u'TRLA_E', u'TRLA', u'CA3', u'CERE2', u'CH31', u'EUMI2', u'FOPU2', u'FRAN2', u'FRBE', u'FRPE3', u'FRPE2', u'GYDI', u'JUSC', u'MAPO', u'MO', u'OTHER', u'PIFL', u'PIPO', u'PIST2', u'PLWR', u'POAN', u'POFR', u'QUMA1', u'SO', u'UNKN', u'VI5', u'ABBA', u'ABCO', u'ABFR', u'AB', u'ACCA', u'ACCAQE', u'ACNI', u'ACPLC', u'ACPLCK', u'ACPS', u'ACRUA', u'ACRUG', u'ACRUOG', u'ACRURS', u'AEHI', u'AE', u'AMCA', u'AMUT', u'ARSP', u'ASTR', u'BEAL', u'BEPA', u'BUSP', u'CABEF', u'CA40', u'CALA', u'CAMO', u'CEJA', u'CORA', u'CO1', u'COAM', u'COCO1', u'CRCRI', u'CRVI', u'CRLA', u'EL1', u'ELUM', u'EUUL', u'EUSP', u'FAGR', u'FA', u'FASYP', u'RHFR', u'FRAMAA', u'FRAMCC', u'FREXH', u'FRNI', u'FROR', u'FROXA', u'FRPES', u'FRQU', u'FR', u'GIBIF2', u'GLTRI', u'GLTRS', u'GLTRS1', u'HISP', u'JUCI', u'JUCO3', u'JUPR', u'LADE', u'LA10', u'LISP', u'LOSP', u'MAAC', u'MAPY', u'OXAR', u'PA19', u'PHAM', u'PIAB', u'PIGL1', u'PIMA', u'PIRU', u'PIBA', u'PIMU', u'PIRE', u'PL3', u'PRHAJO', u'PRPE1', u'PYCAA', u'QUBI', u'QUIM', u'QUMU', u'QUPR', u'QUROF', u'RHCA', u'RHTR', u'ROVI', u'SOAL', u'SPVA2', u'SYSP', u'TA', u'TICOG', u'TITO', u'TITOSS', u'TSCA', u'UNKNL', u'UNKNM', u'UNKNS', u'AL', u'POTR1', u'PRVI', u'QUEL', u'RHSP2', u'RHSP', u'SADI', u'SYRE', u'ACGL', u'ACTA', u'ACFR', u'AM', u'COCO2', u'JUCO1', u'JUMO', u'PIEN', u'PICE', u'PICO', u'POBA', u'POSA', u'POAC5', u'PRPA', u'RHGL', u'RHTY', u'SAAL4', u'SAFR', u'SOAM', u'SOAU', u'THPL', u'UKWN', u'WISI', u'ACDE2', u'ACVE2', u'ALRU2', u'ALAR', u'ARME', u'BEAL2', u'BR', u'CASA5', u'CAJA9', u'CAER', u'CETH', u'CERE', u'CHFU', u'CHLA2', u'CIAU', u'CIPA', u'CONU2', u'COBU', u'CRDO', u'CYSC4', u'DAIM', u'DRDR', u'EUGU', u'EUMA', u'EUPA26', u'EUNY', u'EUPA2', u'EUSM', u'FESE', u'FIBE', u'FIRE4', u'FRCA6', u'FRME2', u'GAEL', u'JA6', u'JUCA1', u'JUOC', u'LAPA', u'LIDE', u'LYRA', u'LYFL', u'PYIO', u'MELE', u'MENE', u'MEST', u'MEEX', u'MOAR', u'MYCA', u'MUPA3', u'MYLA', u'NIGL', u'OPFI', u'PH18', u'PICR', u'PIEU', u'PRPI', u'PRYE', u'PTTR', u'PYSP', u'QUCH', u'RHIN2', u'RHSP1', u'RHOV', u'SALA1', u'SALU', u'SA12', u'SACA', u'SC3', u'SETR', u'STNI', u'TAIM', u'TACH2', u'TABA', u'TIUR', u'TIEU', u'VIJA', u'YUAL', u'YURE', u'YUTO', u'ABHO', u'ACPE', u'ACPLCO', u'ACPLCR', u'ACPLSC', u'ACRUAR', u'ACRUOC', u'ACSA2GR', u'AEOC', u'AECA', u'AMAR', u'ARAR', u'AREX', u'BELE', u'BEPEGR', u'BEPO', u'CAJA', u'CATE', u'CAPU', u'COMA', u'CO2', u'CRCR', u'CRMO2', u'CRJA', u'GIBI(F)', u'HADI', u'HAVI', u'MAAM9', u'MADE', u'MAHA', u'PIPUGL', u'PIGL2', u'PIRI', u'PISE', u'POTR2', u'POGR', u'PONIIT', u'POCA', u'PR2', u'PRMA', u'PRSA', u'PRTR', u'PRVISH', u'PRCI', u'PYCAAR', u'QUAU', u'QULY', u'QUMA2', u'QUPAFA', u'STJA', u'TICOGR', u'TIPL', u'ULCAHO', u'ULPA99', u'ULPR', u'ULSE', u'ULTH', u'ZE', u'ABGR', u'ABLA', u'ABMA', u'ABPI', u'ACCI', u'ACPADI', u'ACPLFA', u'ACPLQE', u'ACRUMO', u'CHNO', u'CHOB', u'CHPI', u'COMA2', u'FASYAT', u'FRLA', u'FROX', u'FRPESG', u'FRPEM', u'ILAQ', u'LAAN2', u'LADEWPE', u'MAMA', u'MAIO', u'MAPUEL', u'PAPE', u'PISI', u'PIAR', u'PICO6', u'PIDE', u'POALPY', u'PRCEKW', u'PRLA', u'PRSEAM', u'PRSESH', u'PRSESO', u'PYCACL', u'SAAM', u'SASC', u'SCVE', u'SYVU', u'TABR', u'TIHE', u'TSHE', u'TSME', u'ULAMLI', u'ACGR', u'ACTR', u'AEFL', u'AEPA', u'AU1', u'BEPL2', u'BEUT2', u'BUDA2', u'CHVI', u'CLTR', u'COAL', u'FORS', u'HA4', u'HACA', u'LA6', u'MABE', u'MATS', u'PRCA2', u'PRTO', u'PYKO', u'ROBA', u'SAGR', u'SERE2', u'TOTA', u'UNKNT', u'ANCH4', u'ARBI', u'ARCO24', u'CAEX', u'CA4', u'CACU8', u'CAST', u'CH', u'COLA18', u'DUER', u'ERBI', u'ERCO', u'ERLY', u'EUER', u'EUCO24', u'FIAL5', u'FIRU', u'FIMI', u'FIWA', u'HALA', u'HACA3', u'LE14', u'MEAR', u'MU5', u'MYCO', u'PALO8', u'PIPI6', u'POHE2', u'PSCA', u'RARI', u'TAMU', u'THPE3', u'TUCA', u'UKNW', u'VITI2', u'ACAN', u'ACFA', u'ACMI', u'ACSA3', u'ACSA', u'ACST', u'CEPR', u'CUGU', u'CYOB', u'EBEB', u'LYMI', u'OLTE', u'CEMI', u'POBAB2', u'PRAL2', u'PRGL2', u'PRPU2', u'PR6', u'PRVE', u'SOSE', u'ABAL', u'ABHO2', u'ACGR3', u'CE7', u'COOB', u'CROX', u'FRMA', u'GLCA', u'LAWA', u'MAAM', u'UNKWN', u'PIAS', u'PIOM', u'PIOR', u'PICE2', u'PIMO3', u'PIWA3', u'PTCO', u'PYFA', u'QUAL3', u'QUSE', u'ULGL', u'ACCO', u'ACKO', u'AGVI14', u'ALMO', u'AMNO4', u'ANIM', u'ANMU', u'ANRE', u'ANSQ', u'ARAL', u'ARAL2', u'ARHE2', u'AVBI', u'AZIN2', u'BAHO3', u'BAPU', u'BA13', u'BABL', u'BERE', u'BIOR', u'BOSP8', u'BO9', u'BUBU', u'CARI9', u'CAIN4', u'CACA73', u'CAMA37', u'CAGR11', u'CARO', u'CANE33', u'CALO', u'CHOL', u'CIVE2', u'CISP2', u'CIGR', u'CIRE3', u'CLRO', u'COVI', u'CORA13', u'COERA2', u'COSE2', u'COSU2', u'COUT', u'CRCU', u'DA2', u'DR', u'ELOR2', u'ERSA11', u'ER15', u'ERVA7', u'ERVAO', u'EUDE', u'FABE', u'ALFA', u'FIMI2', u'FIRE3', u'FIVI3', u'FIDE6', u'GA2', u'GUOF', u'HAPE7', u'HELI9', u'HENY', u'HUCR', u'HYLA15', u'HYVE9', u'ILPA2', u'JUCHS6', u'LASP', u'LELE', u'LICH4', u'MAIN8', u'MAZA', u'MEPO5', u'MICA21', u'MOCI3', u'MOOL', u'MONI', u'MUPA4', u'NOEM', u'OCSE2', u'OCEL', u'ORCO9', u'PASP', u'PATE2', u'PACE8', u'PEPT', u'PH7', u'PIDI3', u'PIRA2', u'PIDU', u'PIAR9', u'PIPE8', u'PLOR80', u'PLPI4', u'PL13', u'PONE21', u'PO3', u'POUS2', u'POLO21', u'PRPA11', u'PRPA2', u'PSEL5', u'PSGU', u'PTIN', u'PTMA8', u'RAMA', u'RORE2', u'PISA2', u'SCPU18', u'SESU4', u'SEGR5', u'SPCA', u'SYCO', u'SYJA', u'TAAR', u'TABA2', u'TADO2', u'TAPA13', u'TECA', u'THPU', u'TITU', u'TOAR2', u'UNID', u'VIPA6']
# probably silly to hardcode these but it's also silly to query the db every call here.

def biomasscalcreq(reqparams, dbconn):
    dbh = 0
    height = 0
    species = ""
    region = ""
    errorlist = []
    biomassresult = []
    try:
        species = reqparams['spec']
        if species not in speclist:
            errorlist.append('Unknown species')
        dbh = float(reqparams['dbh'])
        region = reqparams['region']
        if region not in regionlist:
            errorlist.append('Unknown region')
        height = float(reqparams['ht'])
    except:
        pass
    if len(errorlist) == 0:
        try:
            biomassresult = biomass_calc(dbconn, speccode=species, region=region, dbh=dbh, ht=height)
        except:
            errorlist.append('Biomass calculation error')
    return(biomassresult, errorlist, dbh, height, species, region)

@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def biomasscalc(request):
    if request.method == 'GET':
        dbconn = sqlite3.connect(UrbForDB)
        (biomassresult, errorlist, dbh, height, species, region) = biomasscalcreq(request.query_params, dbconn)
        dbconn.close()
        if len(errorlist) > 0:
            return Response({'errors': errorlist, 'dbh': dbh, 'ht': height, 'species': species, 'region': region})
        else:
            return Response({'biomass': biomassresult[0], 'carbon': biomassresult[1], 'co2': biomassresult[2], 'dbh': dbh, 'ht': height, 'species': species, 'region': region})
            
    elif request.method == 'POST':
        #cats = json.loads(request.data)['cats']
        #return Response({'mycats': cats})
        #return Response(request.data['cats'])
        # Works when I POST {"cats": ["Diego", "Charlie"]} to the interface
        dbconn = sqlite3.connect(UrbForDB)
        if type(request.data) is list:
            outlist = []
            for item in request.data:
                (biomassresult, errorlist, dbh, height, species, region) = biomasscalcreq(item, dbconn)
                if len(errorlist) > 0:
                    outlist.append({'errors': errorlist, 'dbh': dbh, 'ht': height, 'species': species, 'region': region})
                else:
                    outlist.append({'biomass': biomassresult[0], 'carbon': biomassresult[1], 'co2': biomassresult[2], 'dbh': dbh, 'ht': height, 'species': species, 'region': region})
            dbconn.close()
            return Response(outlist)
        elif type(request.data) is dict:
            (biomassresult, errorlist, dbh, height, species, region) = biomasscalcreq(request.data, dbconn)
            dbconn.close()
            if len(errorlist) > 0:
                return Response({'errors': errorlist, 'dbh': dbh, 'ht': height, 'species': species, 'region': region})
            else:
                return Response({'biomass': biomassresult[0], 'carbon': biomassresult[1], 'co2': biomassresult[2], 'dbh': dbh, 'ht': height, 'species': species, 'region': region})
        else:
            return Response({'errors': ['Unknown input format']})
            
# POST [{"spec": "ACRU", "region": "NoCalC", "dbh": 2.8}, {"spec": "ACRU", "region": "NoCalC", "dbh": 4.1}]
