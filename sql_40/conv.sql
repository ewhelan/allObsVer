CREATE VIEW mondb AS
SELECT
    type@desc                  ,
    expver@desc                ,
    class@desc                 ,
    stream@desc                ,
    andate@desc                ,
    antime@desc                ,
    reportype@hdr              ,
    numtsl@desc                ,
    timeslot@timeslot_index    ,
    seqno@hdr                  ,
    bufrtype@hdr               ,
    subtype@hdr                ,
    groupid@hdr                ,
    obstype@hdr                ,
    codetype@hdr               ,
    sensor@hdr                 ,
    statid@hdr                 ,
    date@hdr                   ,
    time@hdr                   ,
    report_status@hdr          ,
    report_event1@hdr          ,
    report_rdbflag@hdr         ,
    degrees(lat) as lat@hdr    ,
    degrees(lon) as lon@hdr    ,
    lsm@modsurf                ,
    orography@modsurf          ,
    stalt@hdr                  ,
    flight_phase@conv          ,
    anemoht@conv               ,
    baroht@conv                ,
    station_type@conv          ,
    sonde_type@conv            ,
    entryno@body               ,
    obsvalue@body              ,
    varno@body                 ,
    vertco_type@body           ,
    vertco_reference_1@body    ,
    datum_anflag@body          ,
    datum_status@body          ,
    datum_event1@body          ,
    datum_rdbflag@body         ,
    biascorr@body              ,
    biascorr_fg@body           ,
    an_depar@body              ,
    fg_depar@body              ,
    obs_error@errstat          ,
    repres_error@errstat       ,
    pers_error@errstat         ,
    fg_error@errstat           ,
    eda_spread@errstat         ,
    mf_vertco_type@body        ,
    mf_log_p@body              ,
    mf_stddev@body
FROM desc,timeslot_index,hdr,modsurf,conv,body,errstat
WHERE obstype>=1 AND obstype<=6;
