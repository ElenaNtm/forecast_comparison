# forecast_comparison
Forecast data comparison
<br>
TIME<br>
Time in METEOGEN prediction data is in UTC <br>
Greek winter time: UTC +2 (Change to winter time, last Sunday of October at 4:00 AM to 3:00 AM)<br>
Greek summer time: UTC +3 (Change to winter time, last Sunday of March at 3:00 AM to 4:00 AM)<br>
<br>
PARKS <br>
Once a park is added to METEOGEN platform it starts with the projections from the begging and not from the day that it was added.<br>


<br>

ANALYSIS ON THE DATA<br>
Do the same work for W+1 and W+6 <br>
Download once the historical data<br>
Convert time from UTC to UTC+2<br>
Drop the columns of UTC time, Radiation and Type (all solar pv)<br>
Group by Asset and save to individual dataframes<br>
Reupload those dataframes and concatenate them to one with each column being the asset<br>
Make KWh and KW to MWh and MW <br>
Aggregate the columns so as to find the aggregated power and energy<br>
Save that to an excel<br>
Continue editing the 5 KPIs and save the file again to new path<br>
Create a dataframe with the 5 KPIs one for each day and in a separate dataframe do it for the week and not only for the day<br>
<br>
TOLERANCE – ΑΝΑ ΒΔΟΜΑΔΑ (ΜΠΟΡΟΥΝ ΝΑ ΓΙΝΟΥΝ ΚΑΙ ΑΝΑ ΜΕΡΑ)<br>
Σταθερές από τον ΑΔΜΗΕ οι οποίες μπορεί να αλλάξουν ανά πάσα στιγμή<br>
<br>

α2ADEV	-0.009<br>
α2RMSDEV	-0.009<br>
α3ADEV	0.28<br>
 α3RMSDEV	0.28<br>
α1ADEV	0.35<br>
α1RMSDEV 	0.4<br>
UNCBALR, ADEV  €/MWh	10<br>
UNCBALR, RMSDEV €/MWh	210<br>
minTOLADEV 	20%<br>
minTOLRMSDEV	20%<br>
maxTOLADEV	100%<br>
maxTOLRMSDEV	100%<br>
maxTOL DEV_NORM	100%<br>
minTOL DEV_NORM	0.05%<br>
α1DEV_NORM	0.27<br>
α2DEV_NORM	0.0109<br>
α3DEV_NORM	0.28<br>
<br>
Στον πίνακα παρουσιάζονται οι σταθερές<br>
Α = (UNCBALR, ADEV  €/MWh *ADEV)*(NADEV - 𝑻𝑶𝑳𝒓,𝑨𝑫𝑬𝑽 (%)) (€)-><br>
A = (10*ADEV)*(NADEV-30.87)<br>
<br>
B = (UNCBALR, RMSDEV €/MWh*RMSDEV)*(NRMSDEV - 𝑻𝑶𝑳𝒓,𝑹𝑴𝑺𝑫𝑬𝑽 (%))(€)-><br>
B = (210*RMSDEV)*(NRMSDEV – 35.87)<br>

𝑻𝑶𝑳𝒓,𝑫𝑬𝑽_NORM (%) = MAX(minTOL DEV_NORM, MIN(maxTOL DEV_NORM, α1DEV_NORM+ α2DEV_NORM *MQ^ α3DEV_NORM)-><br>
𝑻𝑶𝑳𝒓,𝑫𝑬𝑽_NORM (%) =MAX(0.05,MIN(100,0.27-0.0109*MQ^0.28))<br>
<br>
𝑻𝑶𝑳𝒓,𝑨𝑫𝑬𝑽 (%) = MAX(minTOLADEV,MIN(maxTOLADEV, α1ADEV+ α2ADEV*MQ^ α3ADEV))-><br>
𝑻𝑶𝑳𝒓,𝑨𝑫𝑬𝑽 (%) = MAX(100,MIN(100,0.35-0.009*MQ^0.28))<br>
<br>
𝑻𝑶𝑳𝒓,𝑹𝑴𝑺𝑫𝑬𝑽 (%) = MAX(minTOLRMSDEV,MIN(maxTOLRMSDEV, α1RMSDEV+ α2RMSDEV*MQ^ α3RMSDEV))-><br>
𝑻𝑶𝑳𝒓,𝑹𝑴𝑺𝑫𝑬𝑽 (%) = MAX(20,MIN(100,0.4-0.009*MQ^0.28))<br>


<br>
Πληρώνουμε αν-ν:<br>

NCBALR_C1 = 0 <-> A & B <=0<br>
NCBALR_C1 = MAX(A,B)<br>

NCBALR_C2 = 0 <-> ANDEV < 𝑻𝑶𝑳𝒓,𝑫𝑬𝑽_NORM (%)<br>
<br>




Αντίστοιχη διαδικασία ανά πάρκο αυτή την φορά<br>

