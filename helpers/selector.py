from helpers.tools.eaton_exportacion import extract_data_eaton_export
from helpers.tools.eaton_importacion import extract_data_eaton_import
from helpers.tools.estapack_induspac import extract_data_estapack_iduspac
from helpers.tools.estapack_invex import extract_data_estapack_invex
from helpers.tools.estapack_pcm import extract_data_estapack_pcm
from helpers.tools.jabil_exportacion import extract_data_jabil_export
from helpers.tools.jabil_importacion import extract_data_jabil_import
from helpers.tools.lau_importacion import extract_data_lau_import
from helpers.tools.lau_exportacion import extract_data_lau_export
from helpers.tools.mmj_exportacion import extract_data_mmj_export
from helpers.tools.mmj_importacion import extract_data_mmj_import
from helpers.tools.safran_electrical import extract_data_safran
from helpers.tools.signify import extract_data_signify
from helpers.tools.vehicle_stability_exportacion import extract_data_vehicle_stability_export
from helpers.tools.vehicle_stability_importacion import extract_data_vehicle_stability_import
from helpers.tools.modine import getTables
from helpers.tools.ssc import getTables as ssc_getTables
def selectorTemplate(PATH,RFC,TYPE):
    """
    This function is used to select the template to be used for the generation of the RFC.
    """
    if(RFC == "ETE9603221A4") or (RFC=="EIN0306306H6"):
        #search for the word "exportacion" in the text
        try:
            if TYPE=="export":
                extract_data_eaton_export(PATH)
            elif TYPE=="import":
                extract_data_eaton_import(PATH)
        except Exception as e:
            print(e)
            extract_data_eaton_import(PATH)
            pass
    elif(RFC == "EST040824HB5") or (RFC == "PCM9307212B8"):
        if RFC=="PCM9307212B8":
            print("Export template estapack pcm")
            extract_data_estapack_pcm(PATH)
        elif(RFC == "EST0408HB5"):
            print("Template estapack iduspac")
            extract_data_estapack_iduspac(PATH)
            if TYPE == "export":
                print("Export template iduspac")
            else:
                print("Import template iduspac") 
        else:
            print("Template invex")
            extract_data_estapack_invex(PATH)
    elif(RFC == ("JTO181002378") or (RFC=="JMO190130T20") or (RFC=="JGS020701TY0") or  (RFC=="JCM9701315Q6") or (RFC=="JCC000904KK2") or (RFC=="JAM100323UPA")):
        #jabil template
        if TYPE == "export":
            print("Export template jabil")
            extract_data_jabil_export(PATH)
        else:
            print("Import template jabil")
            extract_data_jabil_import(PATH)
    elif(RFC=="RME040213EC5"):
        #lau template
        if TYPE == "export":
            print("Export template lau")
            extract_data_lau_export(PATH)
        else:
            print("Import template lau")
            extract_data_lau_import(PATH)
    elif(RFC == "PME620620E84") or (RFC == "PLM780314167") or (RFC == "PLE910306CHA" or RFC == "PLE880914BW6"):
        #SIGNIFY template   
        if TYPE == "export":
            print("Export template SIGNIFY")
            extract_data_signify(PATH)
        else:
            print("Import template  SIGNIFY")
            extract_data_signify(PATH)

    elif(RFC == "TME940420LV5"):
        #TEGRANT template
        if TYPE == "export":
            print("Export template TEGRANT  ")
            extract_data_safran(PATH)
        else:
            print("Import template TEGRANT")
            extract_data_safran(PATH)

    elif(RFC == "T040824HB5"):
        if TYPE == "export":
            print("Export template TEGRANT  ")
            extract_data_safran(PATH)
        else:
            print("Import template")
            extract_data_safran(PATH)

    elif(RFC == "VST0906151H7")or (RFC == "OIS120807SV8"):
        if TYPE == "export":
            print("Export template")
            
            extract_data_vehicle_stability_export(PATH)
        else:
            print("Import template")
            extract_data_vehicle_stability_import(PATH)
    elif (RFC == "MMJ930128UR6"):
        ##MMJ 
        if TYPE == "export":
            print("Export template MMJ")
            extract_data_mmj_export(PATH)
        else:
            print("Export template  MMJ")
            extract_data_mmj_import(PATH)
            
    elif (RFC == "MTC901210UC2"):
        ##MMJ 
        print("Export template Modine")
    elif (RFC == "SAI120808FA9"):
        modine = getTables(PATH)
        print("Export template Modine")
    elif (RFC == "XEXX010101000"):
        ssc_getTables(PATH)
        
    else:
        
        print("No template found for this RFC:"+RFC)
        