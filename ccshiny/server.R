
# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)
library(rhandsontable)
library(httr)
library(jsonlite)

regions <- c('CenFla','GulfCo','InlEmp','InlVal','InterW', 'LoMidW','MidWst','NMtnPr','NoCalC','NoEast','PacfNW','Piedmt','SoCalC','SWDsrt','TpIntW','Tropic')
speclist <- c('ACSP2','ACNE','ACPA','ACRU','ACWR','ACAC2','ALJU','ALLE','ARHE','ARCU','AVCA','BA','BAVA','BENI','BE','BIJA','BINO','BOSP','BDL OTHER','BDM OTHER','BDS OTHER','BEL OTHER','BEM OTHER','BES OTHER','BRPA','BRSU','BUCA','CAME','CAPU13','CASU34','CAVI','CAPA3','CACA','CATO','CAGL','CAIL','CAOV2','CAOV','CA1','CAMI36','CABI2','CAFI','CASSI','CAEQ','CEDE','CELA','CECA','CHHU','CHSP','CICA','CISP','CLQU','CL6','COUV','CONU','CEL OTHER','CEM OTHER','CES OTHER','COPR','COFL','COCI','CULA','CUAN','CUAR','CUSE','CYCI','CYRE11','DASI','DERE','POPI','DIVI','DYDE2','CHLU','ELDE','ENCY','ERJA','ERCR','EU1','EUUN2','EUTI','FE','FIBE2','FICA','FIEL','FILY','FI1','FRCA','FRPE','GIBI','GLTRIN','LOGO','GRRO','HIMO','HITI','HYLA','ILCO2','ILSP','ILVO','JAMI','JAIN','JUCH','JU','JUSI','KOELFO','LAIN','LIJA','LILU','LIOR','LIST','LITU','LICH','LIDE2','MATE','MAGR','MAST','MAVI','MASO','MAPU','MAIN','MEQU','MEAZ','MYCE','MOAL','MUPA','NEOL','NYSY','PEL OTHER','PEM OTHER','PES OTHER','PAAC','PATO','PEAM','PEBO','PHCA','PHDA4','PHRE','PHRO','PHSY','PHSP2','PHFR','PICL','PIEC','PIEL2','PIPA','PI2','PITA','PIFE','PLOC','THOR','PLAC1','POMA','PONA','PODE','PRAN','PRCA','PRPE2','PRSE1','PR','PYCA','PYCO','QUAC2','QUAL','QUFA','QUGE','QULA','QULA2','QUMI','QUNI','QUPH','QUSH','QU','QUNU','QUVI','RAGL','RHIN62','SAPA','SABA','SANI4','BRAC','SCTE','SEPU7','SIGL','SWMA','SYRO','TACH','TAPA','TASP','TAIN','TAAS','TADI','TACA','TH9','TIGR3','TITI2','TRSE6','ULAL','ULAM','ULPA','ULPU','ULRU','ULS','ULX','UNP','UNS','UNT','VEME','VIOD','VISP2','WAFI','WARO','WOBI2','CULE','YU1','ACBU','ACGI','ACRU_O','ACSA1','ACSA2','AEGL','CASA','CACO','SEBI5','CABI','CHTH','CIAU2','CLLU','COKO','CRPH','EUCI','EUSA','FISI','FOIN3','FRAM','GLTR','HIMU3','HISY','ILCA','ILMY','ILOP','ILOP_S','ILAT','JUNI','JUVI','KOBI','KOPA','LA6_M','LA6_N','LA6_T1','LA6_T2','LISI','MAGR_L','MATR','PYAN','MA2','MEGL','MORU','OSFR','PHSE','PIPU','PICO5','PIEL','PINI','PIST','PIVI','PICH','PLAC_B','PLAC','POAL','PRAM','PRCE','PRSE2','PYCO2','PYCA_B','QUAC','QUCO','QUHE','QUCI','QULA1','QUPA','QURU','QUST','QUVE','ROPS','SAMI8','SAPE12','SAMA_T','SANI','SA','SAAL','THOC','TIAM','TICO','TRFO','ULPA_D','ULPA_E','VIPR','VIAG','WIFL','CULE2','YUGL2','ZESE','ABPR','ACBA2','ACDE','ACLO','ACME','ACMA','ACOB','AECA2','AECA3','AGFL','AIAL','ALCO2','ALGL','ALRH','ARUN','ARMA2','ARRO','BAFO','BEPE','BRAC2','BRDI9','BRPO','BRAR','BRBR','BRED','CATW','CACI','CADE2','CACA3','CAED','CALE','CADE','CASP','CEAT','CEAU','CEOC','CESI4','CESI3','CEOC3','CHLI','CHRE','CHTA','CILI','CISI','COLA','COAU','CRPA','CRRU','DOVI','ERDE','ERCA','EUCA1','EUCI2','EUCL','EUCO3','EUCR','EUFI81','EUGL','EUGLCO','EUGR','EULE2','EULE','EUMA23','EUNI','EUPO','EURO','EURU','EUSI','EUTE','EUTO11','EUVI','FIMA2','FIMINI','FROR2','FRANR','FRUH','FRVE','FRVEG','GEPA','HASU','HEAR','HYFL','ILAL','JUCA2','JURE','KOEL','LANO','LELA12','LIOV','LIFO','LYAS','MATI','MALA6','MAFL80','MASY2','MABO','MELI7','OLEU','OLEU2','CEFL','PIAT','PIBR2','PICA','PICO2','PIED','PIHA','PIMU2','PIPI2','PIRA','PIRO','PITH','PITO2','PIPH2','PIRH','PITO','PIUN','PIVI5','PLRA','POGR2','PONI','POCA2','PRCH','PRAR','PRBL','PRCEKV','PRDO','PRDU','PRIL','PRLY','PSME','PTST','PUGR','PYCA_A','PYKA','QUAG','QUEN','QUIL2','QUKE','QULO','QURO','QUSU','RHIN','ROAMI','SAALT','SAMA','SACANE','SCMO','SCPO','SECO9','SESE','SEGI','SOJA','STSI','SYPA2','TAAV','TACH3','TRCO','TRAC','UMCA','XYCO','YUGU','ZESE_V','ACPL','ACPL_CK','ACPS_S','AC','AECA3_B','AECA3_S','UNKNB','CABE','CABE_F','CE2','CESI2','UNKNC','CRLA80','CR','CUMA','CU','DIKA','ELAN','FASY','FRAM_A','FRAM_R','FRAN_R','FREX','FREX_H','FREX_K','FRHO','FROX_F','FRPE_M','FRPE_P','FRPE_S','FRVE_FW','FRVE_G','GIBI_AG','GIBI_F','GL3','GLTR_S','JUHI','JU1','KOPA_F','MASO_G','MA1','OSVI','PI1','PIPA4','PISY','PIAT4','PICH_PS','PI23','PLAC_C','PLOR','PO','PRAM2','PRAV','PRSU','PYCA_C','PYCA_CH','PYCA_R','PYCA_T','PYCA_W','PY','QUWI','RHLA','ROPS_PR','SOHUCQ','SOHUCF','TI','TRLA_E','TRLA','CA3','CERE2','CH31','EUMI2','FOPU2','FRAN2','FRBE','FRPE3','FRPE2','GYDI','JUSC','MAPO','MO','OTHER','PIFL','PIPO','PIST2','PLWR','POAN','POFR','QUMA1','SO','UNKN','VI5','ABBA','ABCO','ABFR','AB','ACCA','ACCAQE','ACNI','ACPLC','ACPLCK','ACPS','ACRUA','ACRUG','ACRUOG','ACRURS','AEHI','AE','AMCA','AMUT','ARSP','ASTR','BEAL','BEPA','BUSP','CABEF','CA40','CALA','CAMO','CEJA','CORA','CO1','COAM','COCO1','CRCRI','CRVI','CRLA','EL1','ELUM','EUUL','EUSP','FAGR','FA','FASYP','RHFR','FRAMAA','FRAMCC','FREXH','FRNI','FROR','FROXA','FRPES','FRQU','FR','GIBIF2','GLTRI','GLTRS','GLTRS1','HISP','JUCI','JUCO3','JUPR','LADE','LA10','LISP','LOSP','MAAC','MAPY','OXAR','PA19','PHAM','PIAB','PIGL1','PIMA','PIRU','PIBA','PIMU','PIRE','PL3','PRHAJO','PRPE1','PYCAA','QUBI','QUIM','QUMU','QUPR','QUROF','RHCA','RHTR','ROVI','SOAL','SPVA2','SYSP','TA','TICOG','TITO','TITOSS','TSCA','UNKNL','UNKNM','UNKNS','AL','POTR1','PRVI','QUEL','RHSP2','RHSP','SADI','SYRE','ACGL','ACTA','ACFR','AM','COCO2','JUCO1','JUMO','PIEN','PICE','PICO','POBA','POSA','POAC5','PRPA','RHGL','RHTY','SAAL4','SAFR','SOAM','SOAU','THPL','UKWN','WISI','ACDE2','ACVE2','ALRU2','ALAR','ARME','BEAL2','BR','CASA5','CAJA9','CAER','CETH','CERE','CHFU','CHLA2','CIAU','CIPA','CONU2','COBU','CRDO','CYSC4','DAIM','DRDR','EUGU','EUMA','EUPA26','EUNY','EUPA2','EUSM','FESE','FIBE','FIRE4','FRCA6','FRME2','GAEL','JA6','JUCA1','JUOC','LAPA','LIDE','LYRA','LYFL','PYIO','MELE','MENE','MEST','MEEX','MOAR','MYCA','MUPA3','MYLA','NIGL','OPFI','PH18','PICR','PIEU','PRPI','PRYE','PTTR','PYSP','QUCH','RHIN2','RHSP1','RHOV','SALA1','SALU','SA12','SACA','SC3','SETR','STNI','TAIM','TACH2','TABA','TIUR','TIEU','VIJA','YUAL','YURE','YUTO','ABHO','ACPE','ACPLCO','ACPLCR','ACPLSC','ACRUAR','ACRUOC','ACSA2GR','AEOC','AECA','AMAR','ARAR','AREX','BELE','BEPEGR','BEPO','CAJA','CATE','CAPU','COMA','CO2','CRCR','CRMO2','CRJA','GIBI(F)','HADI','HAVI','MAAM9','MADE','MAHA','PIPUGL','PIGL2','PIRI','PISE','POTR2','POGR','PONIIT','POCA','PR2','PRMA','PRSA','PRTR','PRVISH','PRCI','PYCAAR','QUAU','QULY','QUMA2','QUPAFA','STJA','TICOGR','TIPL','ULCAHO','ULPA99','ULPR','ULSE','ULTH','ZE','ABGR','ABLA','ABMA','ABPI','ACCI','ACPADI','ACPLFA','ACPLQE','ACRUMO','CHNO','CHOB','CHPI','COMA2','FASYAT','FRLA','FROX','FRPESG','FRPEM','ILAQ','LAAN2','LADEWPE','MAMA','MAIO','MAPUEL','PAPE','PISI','PIAR','PICO6','PIDE','POALPY','PRCEKW','PRLA','PRSEAM','PRSESH','PRSESO','PYCACL','SAAM','SASC','SCVE','SYVU','TABR','TIHE','TSHE','TSME','ULAMLI','ACGR','ACTR','AEFL','AEPA','AU1','BEPL2','BEUT2','BUDA2','CHVI','CLTR','COAL','FORS','HA4','HACA','LA6','MABE','MATS','PRCA2','PRTO','PYKO','ROBA','SAGR','SERE2','TOTA','UNKNT','ANCH4','ARBI','ARCO24','CAEX','CA4','CACU8','CAST','CH','COLA18','DUER','ERBI','ERCO','ERLY','EUER','EUCO24','FIAL5','FIRU','FIMI','FIWA','HALA','HACA3','LE14','MEAR','MU5','MYCO','PALO8','PIPI6','POHE2','PSCA','RARI','TAMU','THPE3','TUCA','UKNW','VITI2','ACAN','ACFA','ACMI','ACSA3','ACSA','ACST','CEPR','CUGU','CYOB','EBEB','LYMI','OLTE','CEMI','POBAB2','PRAL2','PRGL2','PRPU2','PR6','PRVE','SOSE','ABAL','ABHO2','ACGR3','CE7','COOB','CROX','FRMA','GLCA','LAWA','MAAM','UNKWN','PIAS','PIOM','PIOR','PICE2','PIMO3','PIWA3','PTCO','PYFA','QUAL3','QUSE','ULGL','ACCO','ACKO','AGVI14','ALMO','AMNO4','ANIM','ANMU','ANRE','ANSQ','ARAL','ARAL2','ARHE2','AVBI','AZIN2','BAHO3','BAPU','BA13','BABL','BERE','BIOR','BOSP8','BO9','BUBU','CARI9','CAIN4','CACA73','CAMA37','CAGR11','CARO','CANE33','CALO','CHOL','CIVE2','CISP2','CIGR','CIRE3','CLRO','COVI','CORA13','COERA2','COSE2','COSU2','COUT','CRCU','DA2','DR','ELOR2','ERSA11','ER15','ERVA7','ERVAO','EUDE','FABE','ALFA','FIMI2','FIRE3','FIVI3','FIDE6','GA2','GUOF','HAPE7','HELI9','HENY','HUCR','HYLA15','HYVE9','ILPA2','JUCHS6','LASP','LELE','LICH4','MAIN8','MAZA','MEPO5','MICA21','MOCI3','MOOL','MONI','MUPA4','NOEM','OCSE2','OCEL','ORCO9','PASP','PATE2','PACE8','PEPT','PH7','PIDI3','PIRA2','PIDU','PIAR9','PIPE8','PLOR80','PLPI4','PL13','PONE21','PO3','POUS2','POLO21','PRPA11','PRPA2','PSEL5','PSGU','PTIN','PTMA8','RAMA','RORE2','PISA2','SCPU18','SESU4','SEGR5','SPCA','SYCO','SYJA','TAAR','TABA2','TADO2','TAPA13','TECA','THPU','TITU','TOAR2','UNID','VIPA6')

biomassq <- function(spec, region, dbh, ht) {
  bdf = data.frame(spec=spec, region=region, dbh=dbh, ht=ht)
  bjson = toJSON(bdf)
  bresult <- POST("http://169.237.167.66/carboncalc/api/biomass", body=bjson, content_type_json())
  fromJSON(content(bresult, "text"))
}
  

shinyServer(function(input, output, session) {
  values = reactiveValues()
  
  data = reactive({
    if (!is.null(input$hot)) {
      DF = hot_to_r(input$hot)
    } else {
      if (is.null(values[["DF"]]))
        DF = data.frame(treeid = 1:10, species = rep('QUAG', 10), region = rep('NoCalC', 10),
                        dbh = rep(5,10), height= rep(4,10), biomass=rep(NA,10), carbon=rep(NA,10), co2=rep(NA,10),
                        stringsAsFactors = F)
      else
        DF = values[["DF"]]
    }
    
    biomassd <- biomassq(DF$species, DF$region, DF$dbh, DF$height)
    DF$biomass <- biomassd$biomass
    DF$carbon <- biomassd$carbon
    DF$co2 <- biomassd$co2
    values[["DF"]] = DF
    DF
  })

  output$hot <- renderRHandsontable({
    DF = data()
#     biomassd <- biomassq(DF$species, DF$region, DF$dbh, DF$height)
#     DF$biomass <- biomassd$biomass
#     DF$carbon <- biomassd$carbon
#     DF$co2 <- biomassd$co2
    if (!is.null(DF))
      #rhandsontable(DF, useTypes = as.logical(input$useType), stretchH = "all")
     rhandsontable(DF, useTypes = FALSE, stretchH = "all") %>%
      hot_col("species", type="autocomplete", source=speclist) %>%
      hot_col("region", type="dropdown", source=regions) %>%
      hot_col("biomass", readOnly = TRUE) %>%
      hot_col("carbon", readOnly = TRUE) %>%
      hot_col("co2", readOnly = TRUE)
    
  })
  
  output$download_table <- downloadHandler(
    filename = function() {
           paste('treedata-', Sys.Date(), '.csv', sep='')
        },
         content = function(file) {
           write.csv(data(), file, row.names=FALSE)
         }
  )
})