from celery import shared_task


import csv
from datetime import datetime

from django.db import DatabaseError

from ereturns.rit.models.models import RitSupervision, RitLoadStatus
from ereturns.rit.models.rit_management_models import (
    DDates, ExtTMeDFrxEchPos, ExtTPsDLoanSpResSt, ExtTMeMAssLiabSuppSbs, ExtTMeMAssFor, ExtTMeMAssForObu,
    ExtTMeMAssLiab, ExtTMeMAssLiabObu, ExtTMeMLnaDl, ExtTMeMLnaDlObu, ExtTMeMEbankingEcommerce, ExtTMeMPortInv,
    ExtTMeMPortSurvey, ExtTMeQInvNonResFi, ExtTMeMFrcTrn, ExtTMeMFrcTrnSupp, ExtTMeMLnaRates, ExtTMeMDepoDri,
    ExtTMeDRemittance, ExtTMeQInvForFi1, ExtTMeQInvForFi2, ExtTMeQAcep, ExtTMeMSted, ExtTMeQSmeLoan, ExtTMeQLnaV2,
    ExtTPsDAsliBalances, ExtTPsMInterSa, ExtTPsMInterTrx, ExtTPsMDpstSector, ExtTPsMIntWaiver, ExtTPsMIntRate,
    ExtTPsDLnProv, ExtTPsDSlrCashRes, ExtTPsQLawsSuits, ExtTPsQLnProv, ExtTPsQIntRate, ExtTPsQLnrecPosition,
    ExtTPsQLnrecRecovery, ExtTPsQShDirInfo, ExtTPsQBankDirLoans, ExtTPsQFiDirLoans, ExtTPsMFiMonitorBr,
    ExtTPsMFiMonitorHo, ExtTPsQBaselBsl3, ExtTMeQDepoClsV2, ExtTPsMLiqdtyFi, ExtTPsMReschedLoans, ExtTPsMSlrCrr,
    ExtTPsMWriteOffLoanlease, ExtTMeMInrNonRes, ExtTMeQLtedTransaction
)

# from celery import current_app
# current_app.conf.CELERY_ALWAYS_EAGER = True
# current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

MESSAGE = {
    "SUCCESS": "Data inserted successfully.",
    "FAILURE": "Data insertion Failed.",
    "NOT_DATE": "date_id does not exists.",
    "NOT_FILE": "File not exists.",
    "STATUS_SUCCESS": "Success",
    "STATUS_FAILURE": "Failed",
    "FILTER_ERROR": "Failed to filter previous data.",
    "COUNT_ERROR": "Failed to count the inserted data.",
}


def get_decoded_list(id):
    file = RitSupervision.objects.get(id=id).file
    try:
        decoded_file_string = file.read().decode('utf-8')
    except UnicodeDecodeError as e:
        status = {
            "success": False,
            "msg": str(e)
        }
        return None, status
    decoded_file = decoded_file_string.splitlines()
    status = {
            "success": True,
        }
    return decoded_file, status


def get_fi_reporting_date(decoded_list, fi_index, db):
    reporting_date = decoded_list[2].split(",")[0]
    fi = int(decoded_list[2].split(",")[fi_index])
    date_id = None
    try:
        try:
            formated_date = datetime.strptime(reporting_date, "%d-%b-%y").date()
        except:
            formated_date = datetime.strptime(reporting_date, "%d-%b-%Y").date()
        dates = DDates.objects.using(db).get(cal_date=formated_date)
        date_id = dates.date_id
    except DDates.DoesNotExist as ex:
        return {
            "success": False,
            "msg":  str(ex)
        }
    except DatabaseError as e:
        return {
            "success": False,
            "msg":  str(e)
        }
    return {
            "success": True,
            "date": date_id,
            "fi": fi,
    }


def insert_rit_load_status(meta, job, status, msg, count=0):
    load_status = RitLoadStatus(rit_name=meta["rit"], fi=meta["fi"], branch=meta["branch"], job=job, status=status,
                                msg=msg, count=count)
    load_status.save()


@shared_task
def insert_rit_t_me_d_frx_ech_pos(id, db, meta):
    job = "insert_rit_t_me_d_frx_ech_pos"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 2, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeDFrxEchPos.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using('rit_mngt').delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        ccy_id = row['CCY_ID']
        fi_id = row['FI_ID']
        me_coa = row['ME_COA']
        amount = 0 if row['AMOUNT'] == "" else row['AMOUNT']
        exchange_rate = row['EXCHANGE_RATE']
        open_position_limit = row['Open_Position_Limit']
        rit = ExtTMeDFrxEchPos(dated=date_id, ccy_id=ccy_id, fi_id=fi_id, me_coa=me_coa, amount=amount,
                               exchange_rate=exchange_rate, open_position_limit=open_position_limit)
        objs.append(rit)
    try:
        ExtTMeDFrxEchPos.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeDFrxEchPos.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
            "success": True,
            "count": count,
            "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
                "success": False,
                "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_d_loan_sp_res_st(id, db, meta):
    job = "insert_rit_t_ps_d_loan_sp_res_st"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsDLoanSpResSt.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        facility_type = row['FACILITY_TYPE']
        application_no = row['APPLICATION_NO']
        application_approved = row['APPLICATION_APPROVED']
        outstanding_amount = 0 if row['OUTSTANDING_AMOUNT'] == "" else row['OUTSTANDING_AMOUNT']
        down_payment_amount = 0 if row['DOWN_PAYMENT_AMOUNT'] == "" else row['DOWN_PAYMENT_AMOUNT']
        interest_suspense = 0 if row['INTEREST_SUSPENSE'] == "" else row['INTEREST_SUSPENSE']
        unapplied_interest = 0 if row['UNAPPLIED_INTEREST'] == "" else row['UNAPPLIED_INTEREST']
        interest_waived = 0 if row['INTEREST_WAIVED'] == "" else row['INTEREST_WAIVED']
        amount_rescheduled_exit = 0 if row['AMOUNT_RESCHEDULED_EXIT'] == "" else row['AMOUNT_RESCHEDULED_EXIT']
        rit = ExtTPsDLoanSpResSt(dated=date_id, fi_id=fi_id, facility_type=facility_type,
                                 application_no=application_no, application_approved=application_approved,
                                 outstanding_amount=outstanding_amount, down_payment_amount=down_payment_amount,
                                 interest_suspense=interest_suspense, unapplied_interest=unapplied_interest,
                                 interest_waived=interest_waived, amount_rescheduled_exit=amount_rescheduled_exit)
        objs.append(rit)
    try:
        ExtTPsDLoanSpResSt.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"]
        }
    try:
        count = ExtTPsDLoanSpResSt.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_ass_liab_supp_sbs(id, db, meta):
    job = "insert_rit_t_me_m_ass_liab_supp_sbs"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMAssLiabSuppSbs.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        me_coa = row['ME_COA']
        amount_bdt = row['AMOUNT BDT']
        rit = ExtTMeMAssLiabSuppSbs(dated=date_id, fi_id=fi_id, monetary_coa_id=me_coa, amount_bdt=amount_bdt)
        objs.append(rit)
    try:
        ExtTMeMAssLiabSuppSbs.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMAssLiabSuppSbs.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_ass_for(id, db, meta):
    job = "insert_rit_t_me_m_ass_for"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMAssFor.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        ccy_id = row['CURRENCY']
        monetary_coa_id = row['ME_COA']
        exchange_rate = row['EXCHANGE_RATE']
        amount_bdt = row['AMOUNT FCY']
        rit = ExtTMeMAssFor(dated=date_id, fi_id=fi_id, ccy_id=ccy_id, monetary_coa_id=monetary_coa_id,
                            exchange_rate=exchange_rate, amount_bdt=amount_bdt)
        objs.append(rit)
    try:
        ExtTMeMAssFor.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMAssFor.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_ass_for_obu(id, db, meta):
    job = "insert_rit_t_me_m_ass_for_obu"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMAssForObu.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        ccy_id = row['CURRENCY']
        monetary_coa_id = row['ME_COA']
        exchange_rate = row['EXCHANGE_RATE']
        amount_bdt = row['AMOUNT FCY']
        rit = ExtTMeMAssForObu(dated=date_id, fi_id=fi_id, ccy_id=ccy_id, monetary_coa_id=monetary_coa_id,
                               exchange_rate=exchange_rate, amount_bdt=amount_bdt)
        objs.append(rit)
    try:
        ExtTMeMAssForObu.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMAssForObu.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_ass_liab(id, db, meta):
    job = "insert_rit_t_me_m_ass_liab"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMAssLiab.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        me_coa = row['ME_COA']
        amount_bdt = row['AMOUNT BDT']
        rit = ExtTMeMAssLiab(dated=date_id, fi_id=fi_id, me_coa=me_coa, amount_bdt=amount_bdt)
        objs.append(rit)
    try:
        ExtTMeMAssLiab.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMAssLiab.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_ass_liab_obu(id, db, meta):
    job = "insert_rit_t_me_m_ass_liab_obu"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMAssLiabObu.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        me_coa = row['ME_COA']
        amount_bdt = row['AMOUNT BDT']
        rit = ExtTMeMAssLiabObu(dated=date_id, fi_id=fi_id, me_coa=me_coa, amount_bdt=amount_bdt)
        objs.append(rit)
    try:
        ExtTMeMAssLiabObu.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMAssLiabObu.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_lna_dl(id, db, meta):
    job = "insert_rit_t_me_m_lna_dl"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMLnaDl.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        eco_sector_id = row['ECO_SECTOR_ID']
        eco_purpose_id = row['ECO_PURPOSE_ID']
        prev_outstanding_amount_bdt = row['PREVIOUS_OUTSTANDING_AMOUNT_BDT']
        cur_actual_amount_disbursed = row['CUR_ACTUAL_AMOUNT_DISBURSED']
        cur_interest_amount = row['CUR_INTEREST_AMOUNT']
        cur_recovered_amount = row['CUR_RECOVERED_AMOUNT']
        written_off_amount = row['WRITTEN_OFF_AMOUNT']
        rit = ExtTMeMLnaDl(dated=date_id, fi_id=fi_id, eco_sector_id=eco_sector_id, eco_purpose_id=eco_purpose_id,
                                prev_outstanding_amount_bdt=prev_outstanding_amount_bdt,
                                cur_actual_amount_disbursed=cur_actual_amount_disbursed,
                                cur_interest_amount=cur_interest_amount, cur_recovered_amount=cur_recovered_amount,
                                written_off_amount=written_off_amount)
        objs.append(rit)
    try:
        ExtTMeMLnaDl.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMLnaDl.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_lna_dl_obu(id, db, meta):
    job = "insert_rit_t_me_m_lna_dl_obu"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMLnaDlObu.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        eco_sector_id = row['ECO_SECTOR_ID']
        eco_purpose_id = row['ECO_PURPOSE_ID']
        prev_outstanding_amount_bdt = row['PREVIOUS_OUTSTANDING_AMOUNT_BDT']
        cur_actual_amount_disbursed = row['CUR_ACTUAL_AMOUNT_DISBURSED']
        cur_interest_amount = row['CUR_INTEREST_AMOUNT']
        cur_recovered_amount = row['CUR_RECOVERED_AMOUNT']
        written_off_amount = row['WRITTEN_OFF_AMOUNT']
        rit = ExtTMeMLnaDlObu(dated=date_id, fi_id=fi_id, eco_sector_id=eco_sector_id, eco_purpose_id=eco_purpose_id,
                                prev_outstanding_amount_bdt=prev_outstanding_amount_bdt,
                                cur_actual_amount_disbursed=cur_actual_amount_disbursed,
                                cur_interest_amount=cur_interest_amount, cur_recovered_amount=cur_recovered_amount,
                                written_off_amount=written_off_amount)
        objs.append(rit)
    try:
        ExtTMeMLnaDlObu.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMLnaDlObu.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_ebanking_ecommerce(id, db, meta):
    job = "insert_rit_t_me_m_ebanking_ecommerce"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMEbankingEcommerce.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        coa_id = row['COA_ID']
        data_in_number = row['DATA_IN_NUMBER']
        data_in_text = row['DATA_IN_TEXT']
        rit = ExtTMeMEbankingEcommerce(dated=date_id, fi_id=fi_id, coa_id=coa_id, data_in_number=data_in_number,
                                       data_in_text=data_in_text)
        objs.append(rit)
    try:
        ExtTMeMEbankingEcommerce.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMEbankingEcommerce.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_port_inv(id, db, meta):
    job = "insert_rit_t_me_m_port_inv"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 9, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMPortInv.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        country_id = row['COUNTRY ID']
        product_type_id = row['PRODUCT_TYPE_ID']
        instrument_type_code = row['INSTRUMENT_TYPE_CODE']
        opening_position_amount = row['OPENING_POSITION_AMOUNT']
        purchase_amount = row['PURCHASE_AMOUNT']
        sale_amount = row['SALE_AMOUNT']
        gain_loss = row['GAIN_LOSS']
        closing_position = row['CLOSING_POSITION']
        fi_id = row['FI ID']
        investor_id = row['INVESTOR_ID']
        security_code = row['SECURITY_CODE']
        economic_sector = row['ECONOMIC_SECTOR']
        rit = ExtTMeMPortInv(dated=date_id, country_id=country_id, product_type_id=product_type_id,
                             instrument_type_code=instrument_type_code, opening_position_amount=opening_position_amount,
                             purchase_amount=purchase_amount, sale_amount=sale_amount, gain_loss=gain_loss,
                             closing_position=closing_position, fi_id=fi_id, investor_id=investor_id,
                             security_code=security_code, economic_sector=economic_sector)
        objs.append(rit)
    try:
        ExtTMeMPortInv.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMPortInv.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_port_survey(id, db, meta):
    job = "insert_rit_t_me_m_port_survey"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMPortSurvey.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        investor_id = row['INVESTOR ID']
        nita_coa = row['NITA_COA']
        amount_bdt = row['AMOUNT BDT']
        rit = ExtTMeMPortSurvey(dated=date_id, fi_id=fi_id, investor_id=investor_id, nita_coa=nita_coa,
                                amount_bdt=amount_bdt)
        objs.append(rit)
    try:
        ExtTMeMPortSurvey.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMPortSurvey.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_q_inv_non_res_fi(id, db, meta):
    job = "insert_rit_t_me_q_inv_non_res_fi"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeQInvNonResFi.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI NAME']
        investor_channel = row['INVESTOR CHANNEL']
        company_name = row['COMPANY NAME']
        enterprise_type = row['ENTERPRISE TYPE']
        sector_major_activities = row['SECTOR/MAJOR ACTIVITIES']
        country = row['COUNTRY']
        mecoa_code = row['MECOA CODE']
        product_code = row['PRODUCT CODE']
        opening_position_date = row['OPENING POSITION DATE']
        opening_position = row['OPENING POSITION']
        position_increase = row['POSITION INCREASE']
        position_decrease = row['POSITION DECREASE']
        changes_due_to_exchange_rate = row['CHANGES DUE TO EXCHANGE RATE']
        changes_due_to_price_change = row['CHANGES DUE TO PRICE CHANGE']
        change_due_to_others = row['CHANGE DUE TO OTHERS']
        closing_position_reported = row['CLOSING POSITION REPORTED']
        closing_position_calculated = row['CLOSING POSITION CALCULATED']
        rit = ExtTMeQInvNonResFi(dated=date_id, fi_id=fi_id, investor_channel=investor_channel,
                                 company_name=company_name, enterprise_type=enterprise_type,
                                 sector_major_activities=sector_major_activities, country=country,
                                 mecoa_code=mecoa_code, product_code=product_code,
                                 opening_position_date=opening_position_date, opening_position=opening_position,
                                 position_increase=position_increase, position_decrease=position_decrease,
                                 changes_due_to_exchange_rate=changes_due_to_exchange_rate,
                                 changes_due_to_price_change=changes_due_to_price_change,
                                 change_due_to_others=change_due_to_others,
                                 closing_position_reported=closing_position_reported,
                                 closing_position_calculated=closing_position_calculated)
        objs.append(rit)
    try:
        ExtTMeQInvNonResFi.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeQInvNonResFi.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_frc_trn(id, db, meta):
    job = "insert_rit_t_me_m_frc_trn"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 3, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMFrcTrn.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        ccy_id = row['CCY_ID']
        country_id = row['COUNTRY_ID']
        fi_id = row['FI_ID']
        fi_branch_id = row['FI_BRANCH_ID']
        payrec_purpose_id = row['PAYREC_PURPOSE']
        unit_of_measure = row['UNIT_OF_MEASURE']
        importer_exporter = row['IMPORTER_EXPORTER']
        eco_sector_id = row['ECO_SECTOR_ID']
        encashment_no_company_name = row['ENCASHMENT_NO_COMPANY_NAME']
        amount_fcy = row['AMOUNT_FCY']
        quantity_volume = row['QUANTITY_VOLUME']
        transaction_count = row['TRANSACTION_COUNT']
        encashment_date = row['ENCASHMENT_DATE']
        transaction_date = row['TRANSACTION_DATE']
        serial_no = row['SERIAL_NO']
        rep_type = row['REP_TYPE']
        sched_code = row['SCHED_CODE']
        type_code = row['TYPE_CODE']
        commodity_id = row['COMMODITY_ID']
        rit = ExtTMeMFrcTrn(dated=date_id, ccy_id=ccy_id, country_id=country_id, fi_id=fi_id, fi_branch_id=fi_branch_id,
                            payrec_purpose_id=payrec_purpose_id, unit_of_measure=unit_of_measure,
                            importer_exporter=importer_exporter, eco_sector_id=eco_sector_id,
                            encashment_no_company_name=encashment_no_company_name, amount_fcy=amount_fcy,
                            quantity_volume=quantity_volume, transaction_count=transaction_count,
                            encashment_date=encashment_date, transaction_date=transaction_date, serial_no=serial_no,
                            rep_type=rep_type, sched_code=sched_code, type_code=type_code,commodity_id=commodity_id)
        objs.append(rit)
    try:
        ExtTMeMFrcTrn.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMFrcTrn.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_frc_trn_supp(id, db, meta):
    job = "insert_rit_t_me_m_frc_trn_supp"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMFrcTrnSupp.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        serial_no = row['SERIAL_NO']
        fi_branch_id = row['FI_BRANCH_ID']
        rep_type = row['REP_TYPE']
        sched_code = row['SCHED_CODE']
        type_code = row['TYPE_CODE']
        ccy_id = row['CCY_ID']
        country_id = row['COUNTRY_ID']
        encashment_no_company_name = row['ENCASHMENT_NO_COMPANY_NAME']
        encashment_date = row['ENCASHMENT_DATE']
        importer_exporter = row['IMPORTER_EXPORTER']
        transaction_date = row['TRANSACTION_DATE']
        amount_fcy = row['AMOUNT_FCY']
        exchange_rate = row['EXCHANGE RATE']
        amount = row['AMOUNT 2']
        rit = ExtTMeMFrcTrnSupp(dated=date_id, fi_id=fi_id, serial_no=serial_no, fi_branch_id=fi_branch_id,
                                rep_type=rep_type, sched_code=sched_code, type_code=type_code, ccy_id=ccy_id,
                                country_id=country_id, encashment_no_company_name=encashment_no_company_name,
                                encashment_date=encashment_date, importer_exporter=importer_exporter,
                                transaction_date=transaction_date, amount_fcy=amount_fcy, exchange_rate=exchange_rate,
                                amount=amount)
        objs.append(rit)
    try:
        ExtTMeMFrcTrnSupp.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMFrcTrnSupp.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_lna_rates(id, db, meta):
    job = "insert_rit_t_me_m_lna_rates"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMLnaRates.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        product_type_id = row['PRODUCT_TYPE_ID']
        interest_rate = row['INTEREST_RATE']
        advances_bdt = row['ADVANCES_BDT']
        rit = ExtTMeMLnaRates(dated=date_id, fi_id=fi_id, product_type_id=product_type_id, interest_rate=interest_rate,
                              advances_bdt=advances_bdt)
        objs.append(rit)
    try:
        ExtTMeMLnaRates.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMLnaRates.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_depo_dri(id, db, meta):
    job = "insert_rit_t_me_m_depo_dri"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMDepoDri.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        product_type_id = row['PRODUCT_TYPE_ID']
        balance_bdt = row['BALANCE_BDT']
        interest_rate = row['INTEREST_RATE']
        rit = ExtTMeMDepoDri(dated=date_id, fi_id=fi_id, product_type_id=product_type_id, balance_bdt=balance_bdt,
                             interest_rate=interest_rate)
        objs.append(rit)
    try:
        ExtTMeMDepoDri.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMDepoDri.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_d_remittance(id, db, meta):
    job = "insert_rit_t_me_d_remittance"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeDRemittance.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI NAME']
        serial_no = row['SERIAL NO']
        fi_branch_id = row['AD FI BRANCH']
        rep_type = row['REPORT TYPE']
        sched_code = row['SCHEDULE CODE']
        type_code = row['TYPE CODE']
        payrec_purpose_id = row['PURPOSE CODE']
        ccy_id = row['CURRENCY']
        country_id = row['COUNTRY']
        district_id = row['DISTRICT']
        nid = row['NID']
        passport = row['PASSPORT']
        amount_fcy = row['AMOUNT FCY']
        rit = ExtTMeDRemittance(dated=date_id, fi_id=fi_id, serial_no=serial_no, fi_branch_id=fi_branch_id,
                                rep_type=rep_type, sched_code=sched_code, type_code=type_code,
                                payrec_purpose_id=payrec_purpose_id, ccy_id=ccy_id, country_id=country_id,
                                district_id=district_id, nid=nid, passport=passport, amount_fcy=amount_fcy)
        objs.append(rit)
    try:
        ExtTMeDRemittance.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeDRemittance.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_q_inv_for_fi_1(id, db, meta):
    job = "insert_rit_t_me_q_inv_for_fi_1"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeQInvForFi1.objects.using(db).filter(dated=date_id, fi_name=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_name = row['FI NAME']
        investor_channel = row['INVESTOR CHANNEL']
        company_name = row['COMPANY NAME']
        legal_enterprise = row['LEGAL FORM OF ENTERPRISE']
        enterprise_type = row['ENTERPRISE TYPE']
        enterprise_location = row['ENTERPRISE LOCATION']
        sector_major_activities = row['SECTOR OF MAJOR ACTIVITIES']
        date_incorporation_reg = row['DATE OF INCORPORATION/REGISTRATION']
        date_of_imp = row['DATE OF IMPLEMENTATION']
        fellow_enterprise = row['FELLOW ENTERPRISE']
        location_fellow_ent = row['LOCATION OF FELLOW ENTERPRISE']
        location_common_parent = row['LOCATION OF COMMON PARENT']
        investor_name = row['INVESTOR NAME']
        country = row['COUNTRY']
        percentage_equity_share = row['PERCENTAGE OF EQUITY SHARE']
        total_foreign_inv_bdt = row['TOTAL FOREIGN EQUITY INVESTMENT AMT (BDT)']
        total_external_debt = row['TOTAL EXTERNAL DEBT']
        total_paid_up = row['TOTAL PAID UP CAPITAL']
        import_date = row['IMPORT DATE']
        imported_by = row['IMPORTED BY']
        imp_amount = row['MACH/EQUIP IMP AMOUNT']
        capital_contribution = row['AS CAPITAL CONTRIBUTION']
        number_foreign_employee = row['NUMBER OF FOREIGN EMPLOYEE']
        num_local_employee = row['NUMBER OF LOCAL EMPLOYEE']
        other_bank = row['OTHER RELATED BANK']
        rit = ExtTMeQInvForFi1(dated=date_id, fi_name=fi_name, investor_channel=investor_channel,
                               company_name=company_name, legal_enterprise=legal_enterprise,
                               enterprise_type=enterprise_type, enterprise_location=enterprise_location,
                               sector_major_activities=sector_major_activities,
                               date_incorporation_reg=date_incorporation_reg, date_of_imp=date_of_imp,
                               fellow_enterprise=fellow_enterprise, location_fellow_ent=location_fellow_ent,
                               location_common_parent=location_common_parent, investor_name=investor_name,
                               country=country, percentage_equity_share=percentage_equity_share,
                               total_foreign_inv_bdt=total_foreign_inv_bdt, total_external_debt=total_external_debt,
                               total_paid_up=total_paid_up, import_date=import_date, imported_by=imported_by,
                               imp_amount=imp_amount, capital_contribution=capital_contribution,
                               number_foreign_employee=number_foreign_employee, num_local_employee=num_local_employee,
                               other_bank=other_bank)
        objs.append(rit)
    try:
        ExtTMeQInvForFi1.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeQInvForFi1.objects.using(db).filter(dated=date_id, fi_name=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_q_inv_for_fi_2(id, db, meta):
    job = "insert_rit_t_me_q_inv_for_fi_2"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeQInvForFi2.objects.using(db).filter(dated=date_id, fi_name=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_name = row['FI NAME']
        investor_channel = row['INVESTOR CHANNEL']
        company_name = row['COMPANY NAME']
        sector_major_activities = row['SECTOR/MAJOR ACTIVITIES']
        legal_enterprise = row['LEGAL FORM OF ENTERPRISE']
        date_of_imp = row['DATE OF IMPLEMENTATION']
        location_ent = row['ENTERPRISE LOCATION']
        total_paid_up = row['TOTAL PAID UP CAPITAL']
        name_invst_ent_abroad = row['NAME INVESTMENT ENTERPRISE ABROAD']
        country_invst_ent_abroad = row['COUNTRY INVESTMENT ENTERPRISE ABROAD']
        percentage_equity_share = row['PERCENTAGE OF EQUITY SHARE INVESTMENT ENTERPRISE ABROAD']
        legal_form_invst_ent_abroad = row['LEGAL FORM INVESTMENT ENTERPRISE ABROAD']
        sect_maj_act_invst_ent_abrd = row['SECTOR OF MAJOR ACTIVITIES INVESTMENT ENTERPRISE ABROAD']
        date_of_imp_invst_ent_abroad = row['DATE OF IMPLEMENTATION INVESTMENT ENTERPRISE ABROAD']
        tot_equity_invst_abrd_amount = row['TOTAL EQUITY INVESTMENT ABROAD AMT (BDT)']
        tot_paid_up_invst_ent_abrd = row['TOTAL PAID UP CAPITAL INVESTMENT ENTERPRISE ABROAD']
        fellow_enterprise = row['FELLOW ENTERPRISE']
        location_fellow_enterprise = row['LOCATION OF FELLOW ENTERPRISE']
        location_common_parent = row['LOCATION OF COMMON PARENT']

        rit = ExtTMeQInvForFi2(dated=date_id, fi_name=fi_name, investor_channel=investor_channel,
                               company_name=company_name, sector_major_activities=sector_major_activities,
                               legal_enterprise=legal_enterprise, date_of_imp=date_of_imp, location_ent=location_ent,
                               total_paid_up=total_paid_up, name_invst_ent_abroad=name_invst_ent_abroad,
                               country_invst_ent_abroad=country_invst_ent_abroad,
                               percentage_equity_share=percentage_equity_share,
                               legal_form_invst_ent_abroad=legal_form_invst_ent_abroad,
                               sect_maj_act_invst_ent_abrd=sect_maj_act_invst_ent_abrd,
                               date_of_imp_invst_ent_abroad=date_of_imp_invst_ent_abroad,
                               tot_equity_invst_abrd_amount=tot_equity_invst_abrd_amount,
                               tot_paid_up_invst_ent_abrd=tot_paid_up_invst_ent_abrd,
                               fellow_enterprise=fellow_enterprise,
                               location_fellow_enterprise=location_fellow_enterprise,
                               location_common_parent=location_common_parent)
        objs.append(rit)
    try:
        ExtTMeQInvForFi2.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeQInvForFi2.objects.using(db).filter(dated=date_id, fi_name=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_q_acep(id, db, meta):
    job = "insert_rit_t_me_q_acep"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeQAcep.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        purpose_type_id = row['PURPOSE_TYPE_ID']
        economic_sector_id = row['ECONOMIC_SECTOR_ID']
        sanction_limit = row['SANCTION_LIMIT']
        disbursement_amount = row['DISBURSEMENT_AMOUNT']
        recovery_amount = row['RECOVERY_AMOUNT']
        classified_amount_ss = row['CLASSIFIED_AMOUNT(SS)']
        classified_amount_df = row['CLASSIFIED_AMOUNT(DF)']
        classified_amount_b_l = row['CLASSIFIED_AMOUNT(B/L)']
        unclassified_amount_sma = row['UNCLASSIFIED_AMOUNT(SMA)']
        unclassified_amount_std = row['UNCLASSIFIED_AMOUNT(STD)']
        overdue_amount = row['OVERDUE_AMOUNT']

        rit = ExtTMeQAcep(dated=date_id, fi_id=fi_id, purpose_type_id=purpose_type_id,
                          economic_sector_id=economic_sector_id, sanction_limit=sanction_limit,
                          disbursement_amount=disbursement_amount, recovery_amount=recovery_amount,
                          classified_amount_ss=classified_amount_ss, classified_amount_df=classified_amount_df,
                          classified_amount_b_l=classified_amount_b_l, unclassified_amount_sma=unclassified_amount_sma,
                          unclassified_amount_std=unclassified_amount_std, overdue_amount=overdue_amount)
        objs.append(rit)
    try:
        ExtTMeQAcep.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeQAcep.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_sted(id, db, meta):
    job = "insert_rit_t_me_m_sted"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 2, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMSted.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        serial_no = row['Serial No.']
        fi_id = row['FI ID']
        fi_branch_id = row['Branch Name']
        debtor_name = row['Debtor Name']
        instrument_classification = row['Instrument Classification*']
        tradable_item = row['Commodity Code']
        creditor_name = row['Creditor Name']
        creditor_type = row['Creditor Type**']
        country_id = row['Creditor Country']
        all_cost_percent_annum = row['All in cost  including other charges (percent per annum)']
        interest_rate = row['Interest Rate (percent per annum)']
        currency_id = row['Currency']
        total_borrowing_amount = row['Total Borrowing Amount']
        f_drawing_disb_date = row['First Drawing / Disbursement Date']
        l_principal_pay_date = row['Last Principal Payment Date']
        maturity_in_days = row['Maturity (in days)']
        opening_pos_principal_outs = row['Opening Position']
        amount_drawn_during_rep_mon = row['Amount Drawn  during the reporting month']
        principal_paid_dur_rep_mon = row['Principal Paid during the reporting month']
        interest_paid_dur_rep_mon = row['Interest Paid during the reporting month']
        others_fees_rep_mon = row['Any other fees & expenses Paid during the reporting month']
        overdue_amount = row['Overdue amount']
        closing_position = row['Closing position']
        lc_no = row['LC No. (if trade credit)/EXP No.']
        remarks = row['Remarks (if any)']
        rit = ExtTMeMSted(dated=date_id, serial_no=serial_no, fi_id=fi_id, fi_branch_id=fi_branch_id,
                          debtor_name=debtor_name, instrument_classification=instrument_classification,
                          tradable_item=tradable_item, creditor_name=creditor_name, creditor_type=creditor_type,
                          country_id=country_id, all_cost_percent_annum=all_cost_percent_annum,
                          interest_rate=interest_rate, currency_id=currency_id,
                          total_borrowing_amount=total_borrowing_amount, f_drawing_disb_date=f_drawing_disb_date,
                          l_principal_pay_date=l_principal_pay_date, maturity_in_days=maturity_in_days,
                          opening_pos_principal_outs=opening_pos_principal_outs,
                          amount_drawn_during_rep_mon=amount_drawn_during_rep_mon,
                          principal_paid_dur_rep_mon=principal_paid_dur_rep_mon,
                          interest_paid_dur_rep_mon=interest_paid_dur_rep_mon, others_fees_rep_mon=others_fees_rep_mon,
                          overdue_amount=overdue_amount, closing_position=closing_position, lc_no=lc_no,
                          remarks=remarks)
        objs.append(rit)
    try:
        ExtTMeMSted.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMSted.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_q_sme_loan(id, db, meta):
    job = "insert_rit_t_me_q_sme_loan"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeQSmeLoan.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI Name']
        sme_category = row['SME Category']
        sub_sector = row['Sub Sector']
        ln_segregation = row['Loan Segregation']
        nature_of_enterprise = row['Nature of Enterprise']
        number_of_enterprise = row['Number of Enterprise']
        disbursement = row['Disbursement']
        outstanding = row['Outstanding']
        ln_recovery = row['Recovery']
        classified = row['Classified']
        amount_others = row['Amount (Others)']
        rit = ExtTMeQSmeLoan(
            dated=date_id,
            fi_id=fi_id,
            sme_category=sme_category,
            sub_sector=sub_sector,
            ln_segregation=ln_segregation,
            nature_of_enterprise=nature_of_enterprise,
            number_of_enterprise=number_of_enterprise,
            disbursement=disbursement,
            outstanding=outstanding,
            ln_recovery=ln_recovery,
            classified=classified,
            amount_others=amount_others
        )
        objs.append(rit)
    try:
        ExtTMeQSmeLoan.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeQSmeLoan.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_q_lna_v2(id, db, meta):
    job = "insert_rit_t_me_q_sme_loan"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeQLnaV2.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        fi_branch_id = row['FI_BRANCH_ID']
        account_number = row['ACCOUNT_NUMBER']
        account_holder_name = row['ACCOUNT_HOLDER_NAME']
        gender_code = row['GENDER_CODE']
        eco_sector_id = row['ECO_SECTOR_ID']
        eco_purpose_id = row['ECO_PURPOSE_ID']
        industry_scale_id = row['INDUSTRY_SCALE_ID']
        collateral_id = row['COLLATERAL_ID']
        product_type_id = row['PRODUCT_TYPE_ID']
        loan_class_id = row['LOAN_CLASS_ID']
        interest_rate = row['INTEREST_RATE']
        sanction_amount = row['SANCTION_AMOUNT']
        opening_balance = row['OPENING_BALANCE']
        disbursed_amount = row['DISBURSED_AMOUNT']
        recovered_amount = row['RECOVERED_AMOUNT']
        accrued_interest = row['ACCRUED_INTEREST']
        other_charges = row['OTHER_CHARGES']
        adjustment_amount = row['ADJUSTMENT_AMOUNT']
        write_off_amount = row['WRITE_OFF_AMOUNT']
        outstanding_amount = row['OUTSTANDING_AMOUNT']
        overdue_amount = row['OVERDUE_AMOUNT']
        rit = ExtTMeQLnaV2(
            dated=date_id,
            fi_id=fi_id,
            fi_branch_id=fi_branch_id,
            account_number=account_number,
            account_holder_name=account_holder_name,
            gender_code=gender_code,
            eco_sector_id=eco_sector_id,
            eco_purpose_id=eco_purpose_id,
            industry_scale_id=industry_scale_id,
            collateral_id=collateral_id,
            product_type_id=product_type_id,
            loan_class_id=loan_class_id,
            interest_rate=interest_rate,
            sanction_amount=sanction_amount,
            opening_balance=opening_balance,
            disbursed_amount=disbursed_amount,
            recovered_amount=recovered_amount,
            accrued_interest=accrued_interest,
            other_charges=other_charges,
            adjustment_amount=adjustment_amount,
            write_off_amount=write_off_amount,
            outstanding_amount=outstanding_amount,
            overdue_amount=overdue_amount
        )
        objs.append(rit)
    try:
        ExtTMeQLnaV2.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeQLnaV2.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_d_asli_balances(id, db, meta):
    job = "insert_rit_t_ps_d_asli_balances"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsDAsliBalances.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        eco_sector_id = row['ECO_SECTOR_ID']
        ps_coa = row['PS_COA']
        freq_ind_code = row['FREQ_IND_CODE']
        amount_bdt = row['AMOUNT_BDT']
        debit_credit_ind_code = row['DEBIT_CREDIT_IND_CODE']
        amount_usd = row['AMOUNT_USD']
        banking_class = row['BANKING_CLASS']
        rit = ExtTPsDAsliBalances(
            dated=date_id,
            fi_id=fi_id,
            eco_sector_id=eco_sector_id,
            ps_coa=ps_coa,
            freq_ind_code=freq_ind_code,
            amount_bdt=amount_bdt,
            debit_credit_ind_code=debit_credit_ind_code,
            amount_usd=amount_usd,
            banking_class=banking_class
        )
        objs.append(rit)
    try:
        ExtTPsDAsliBalances.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsDAsliBalances.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_inter_sa(id, db, meta):
    job = "insert_rit_t_ps_m_inter_sa"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMInterSa.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        aging_range_id = row['AGING_RANGE_ID']
        account_type_code = row['ACCOUNT_TYPE_CODE']
        freq_ind_code = row['FREQ_IND_CODE']
        amount_bdt = row['AMOUNT_BDT']
        no_of_accounts = row['NO_OF_ACCOUNTS']
        rit = ExtTPsMInterSa(
            dated=date_id,
            fi_id=fi_id,
            aging_range_id=aging_range_id,
            account_type_code=account_type_code,
            freq_ind_code=freq_ind_code,
            amount_bdt=amount_bdt,
            no_of_accounts=no_of_accounts
        )
        objs.append(rit)
    try:
        ExtTPsMInterSa.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMInterSa.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_inter_trx(id, db, meta):
    job = "insert_rit_t_ps_m_inter_trx"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMInterTrx.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        orig_fi_branch_id = row['ORIG_FI_BRANCH_ID']
        resp_fi_branch_id = row['RESP_FI_BRANCH_ID']
        unrecon_start = row['UNRECON_START']
        unrecon_end = row['UNRECON_END']
        debit_credit_ind_code = row['DEBIT_CREDIT_IND_CODE']
        aging_range_id = row['AGING_RANGE_ID']
        freq_ind_code = row['FREQ_IND_CODE']
        remarks = row['REMARKS']
        transaction_count = row['TRANSACTION_COUNT']
        amount_bdt = row['AMOUNT_BDT']
        advice_no = row['ADVICE_NO']
        rit = ExtTPsMInterTrx(
            dated=date_id,
            fi_id=fi_id,
            orig_fi_branch_id=orig_fi_branch_id,
            resp_fi_branch_id=resp_fi_branch_id,
            unrecon_start=unrecon_start,
            unrecon_end=unrecon_end,
            debit_credit_ind_code=debit_credit_ind_code,
            aging_range_id=aging_range_id,
            freq_ind_code=freq_ind_code,
            remarks=remarks,
            transaction_count=transaction_count,
            amount_bdt=amount_bdt,
            advice_no=advice_no
        )
        objs.append(rit)
    try:
        ExtTPsMInterTrx.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMInterTrx.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_dpst_sector(id, db, meta):
    job = "insert_rit_t_ps_m_dpst_sector"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMDpstSector.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        eco_sector_id = row['ECO_SECTOR_ID']
        product_type_id = row['PRODUCT_TYPE_ID']
        amount_bdt = row['AMOUNT_BDT']
        reporting_area_code = row['REPORTING_AREA']
        rit = ExtTPsMDpstSector(
            dated=date_id,
            fi_id=fi_id,
            eco_sector_id=eco_sector_id,
            product_type_id=product_type_id,
            amount_bdt=amount_bdt,
            reporting_area_code=reporting_area_code
        )
        objs.append(rit)
    try:
        ExtTPsMDpstSector.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMDpstSector.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_int_waiver(id, db, meta):
    job = "insert_rit_t_ps_m_int_waiver"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMIntWaiver.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        remarks = row['REMARKS']
        waiver_amt_charge_debit_ac = row['WAIVER_AMT_CHARGE_DEBIT_AC']
        waiver_amt_charge_debit_int_su = row['WAIVER_AMT_CHARGE_DEBIT_INT_SUSPENSE']
        uncharged = row['UNCHARGED']
        no_of_loan_accounts = row['NO_OF_LOAN_ACCOUNTS']
        rit = ExtTPsMIntWaiver(
            dated=date_id,
            fi_id=fi_id,
            remarks=remarks,
            waiver_amt_charge_debit_ac=waiver_amt_charge_debit_ac,
            waiver_amt_charge_debit_int_su=waiver_amt_charge_debit_int_su,
            uncharged=uncharged,
            no_of_loan_accounts=no_of_loan_accounts
        )
        objs.append(rit)
    try:
        ExtTPsMIntWaiver.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMIntWaiver.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_int_rate(id, db, meta):
    job = "insert_rit_t_ps_m_int_rate"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMIntRate.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        product_type_id = row['PRODUCT_TYPE_ID']
        eco_sector_id = row['ECO_SECTOR_ID']
        remarks = row['REMARKS']
        highest_interest_rate = row['HIGHEST_INTEREST_RATE']
        lowest_interest_rate = row['LOWEST_INTEREST_RATE']
        freq_ind_code = row['FREQ_IND_CODE']
        bank_classification = row['BANK_CLASSIFICATION']
        rit = ExtTPsMIntRate(
            dated=date_id,
            fi_id=fi_id,
            product_type_id=product_type_id,
            eco_sector_id=eco_sector_id,
            remarks=remarks,
            highest_interest_rate=highest_interest_rate,
            lowest_interest_rate=lowest_interest_rate,
            freq_ind_code=freq_ind_code,
            bank_classification=bank_classification,
        )
        objs.append(rit)
    try:
        ExtTPsMIntRate.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMIntRate.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_d_ln_prov(id, db, meta):
    job = "insert_rit_t_ps_d_ln_prov"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsDLnProv.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        fi_branch_id = row['FI_BRANCH_ID']
        product_type_id = row['PRODUCT_TYPE_ID']
        loan_class_id = row['LOAN_CLASS_ID']
        aging_range_id = row['AGING_RANGE_ID']
        freq_ind_code = row['FREQ_IND_CODE']
        amt_provision_reqd = row['AMT_PROVISION_REQD']
        interest_suspense = row['INTEREST_SUSPENSE']
        actual_provision = row['ACTUAL_PROVISION']
        base_for_provision = row['BASE_FOR_PROVISION']
        outstanding_amount_bdt = row['OUTSTANDING_AMOUNT_BDT']
        insterest_suspense_against_sma = row['SME_AMOUNT_BDT']
        value_of_eligible_securities = row['VALUE_OF_ELIGIBLE_SECURITIES']
        rit = ExtTPsDLnProv(
            dated=date_id,
            fi_id=fi_id,
            fi_branch_id=fi_branch_id,
            product_type_id=product_type_id,
            loan_class_id=loan_class_id,
            aging_range_id=aging_range_id,
            freq_ind_code=freq_ind_code,
            amt_provision_reqd=amt_provision_reqd,
            interest_suspense=interest_suspense,
            actual_provision=actual_provision,
            base_for_provision=base_for_provision,
            outstanding_amount_bdt=outstanding_amount_bdt,
            insterest_suspense_against_sma=insterest_suspense_against_sma,
            value_of_eligible_securities=value_of_eligible_securities
        )
        objs.append(rit)
    try:
        ExtTPsDLnProv.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsDLnProv.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_d_slr_cash_res(id, db, meta):
    job = "insert_rit_t_ps_d_slr_cash_res"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsDSlrCashRes.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        ps_coa = row['PS_COA']
        balance_bdt = row['BALANCE_BDT']
        maintenance_date = row['MAINTENANCE_DATE']
        min_liquid_assets_reqd = row['MIN_LIQUID_ASSETS_REQD']
        surplus_deficit = row['SURPLUS_DEFICIT']
        rit = ExtTPsDSlrCashRes(
            dated=date_id,
            fi_id=fi_id,
            ps_coa=ps_coa,
            balance_bdt=balance_bdt,
            maintenance_date=maintenance_date,
            min_liquid_assets_reqd=min_liquid_assets_reqd,
            surplus_deficit=surplus_deficit
        )
        objs.append(rit)
    try:
        ExtTPsDSlrCashRes.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsDSlrCashRes.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_q_laws_suits(id, db, meta):
    job = "insert_rit_t_ps_q_laws_suits"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsQLawsSuits.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        lawsuit_type_code = row['LAWSUIT_TYPE_CODE']
        case_type_code = row['CASE_TYPE_CODE']
        pending_period = row['PENDING_PERIOD']
        amount_claimed = row['AMOUNT CLAMED']
        actual_recovery = row['ACTUAL RECOVERY']
        suit_count = row['NUMBER OF SUITS']
        remarks = row['REMARKS']
        rit = ExtTPsQLawsSuits(
            dated=date_id,
            fi_id=fi_id,
            lawsuit_type_code=lawsuit_type_code,
            case_type_code=case_type_code,
            pending_period=pending_period,
            amount_claimed=amount_claimed,
            actual_recovery=actual_recovery,
            suit_count=suit_count,
            remarks=remarks
        )
        objs.append(rit)
    try:
        ExtTPsQLawsSuits.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsQLawsSuits.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_q_ln_prov(id, db, meta):
    job = "insert_rit_t_ps_q_ln_prov"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsQLnProv.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        fi_branch_id = row['FI_BRANCH_ID']
        product_type_id = row['PRODUCT_TYPE_ID']
        loan_class_id = row['LOAN_CLASS_ID']
        aging_range_id = row['AGING_RANGE_ID']
        freq_ind_code = row['FREQ_IND_CODE']
        amt_provision_reqd = row['AMT_PROVISION_REQD']
        interest_suspense = row['INTEREST_SUSPENSE']
        actual_provision = row['ACTUAL_PROVISION']
        base_for_provision = row['BASE_FOR_PROVISION']
        outstanding_amount_bdt = row['OUTSTANDING_AMOUNT']
        defaulted_outstanding = row['DEFAULTED_OUTSTANDING']
        insterest_suspense_against_sma = row['INSTEREST_SUSPENSE_AGAINST_SMA']
        value_of_eligible_securities = row['VALUE_OF_ELIGIBLE_SECURITIES']
        report_type_code = row['REPORT_TYPE_CODE']
        rit = ExtTPsQLnProv(
            dated=date_id,
            fi_id=fi_id,
            fi_branch_id=fi_branch_id,
            product_type_id=product_type_id,
            loan_class_id=loan_class_id,
            aging_range_id=aging_range_id,
            freq_ind_code=freq_ind_code,
            amt_provision_reqd=amt_provision_reqd,
            interest_suspense=interest_suspense,
            actual_provision=actual_provision,
            base_for_provision=base_for_provision,
            outstanding_amount_bdt=outstanding_amount_bdt,
            defaulted_outstanding=defaulted_outstanding,
            insterest_suspense_against_sma=insterest_suspense_against_sma,
            value_of_eligible_securities=value_of_eligible_securities,
            report_type_code=report_type_code
        )
        objs.append(rit)
    try:
        ExtTPsQLnProv.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsQLnProv.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_q_int_rate(id, db, meta):
    job = "insert_rit_t_ps_q_int_rate"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsQIntRate.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        product_type_id = row['PRODUCT_TYPE_ID']
        eco_sector_id = row['ECO_SECTOR_ID']
        remarks = row['REMARKS']
        highest_interest_rate = row['HIGHEST_INTEREST_RATE']
        lowest_interest_rate = row['LOWEST_INTEREST_RATE']
        freq_ind_code = row['FREQ_IND_CODE']
        bank_classification = row['BANK_CLASSIFICATION']
        rit = ExtTPsQIntRate(
            dated=date_id,
            fi_id=fi_id,
            product_type_id=product_type_id,
            eco_sector_id=eco_sector_id,
            remarks=remarks,
            highest_interest_rate=highest_interest_rate,
            lowest_interest_rate=lowest_interest_rate,
            freq_ind_code=freq_ind_code,
            bank_classification=bank_classification,
        )
        objs.append(rit)
    try:
        ExtTPsQIntRate.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsQIntRate.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_q_lnrec_position(id, db, meta):
    job = "insert_rit_t_ps_q_lnrec_position"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsQLnrecPosition.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        product_type_id = row['PRODUCT_TYPE_ID']
        eco_sector_id = row['ECO_SECTOR_ID']
        amount_bdt = row['PREV_QTR_BALANCES']
        curr_qtr_balance = row['CURR_QTR_BALANCE']
        prev_qtr_cum_overdues = row['PREV_QTR_CUMM_OVERDUES']
        curr_dues_recoverable = row['CURR_DUES_RECOVERABLE']
        loan_realised_cum_overdues = row['REALISED_CUMM_OVERDUES']
        loan_realised_rec_dues = row['REALISED_CURR_DUES']
        rit = ExtTPsQLnrecPosition(
            dated=date_id,
            fi_id=fi_id,
            product_type_id=product_type_id,
            eco_sector_id=eco_sector_id,
            amount_bdt=amount_bdt,
            curr_qtr_balance=curr_qtr_balance,
            prev_qtr_cum_overdues=prev_qtr_cum_overdues,
            curr_dues_recoverable=curr_dues_recoverable,
            loan_realised_cum_overdues=loan_realised_cum_overdues,
            loan_realised_rec_dues=loan_realised_rec_dues,
        )
        objs.append(rit)
    try:
        ExtTPsQLnrecPosition.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsQLnrecPosition.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_q_lnrec_recovery(id, db, meta):
    job = "insert_rit_t_ps_q_lnrec_recovery"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsQLnrecRecovery.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_ID']
        ps_coa = row['PS_COA']
        product_type_id = row['PRODUCT_TYPE_ID']
        loan_class_id = row['LOAN_CLASS_ID']
        remarks = row['REMARKS']
        loan_amt_bdt = row['LOAN_AMT_BDT']
        written_off_amount = row['WRITTEN_OFF_AMOUNT']
        cash_recovery = row['CASH_RECOVERY']
        new_classified_advance = row['NEW_CLASSIFIED_ADVANCE']
        resched_amount = row['RESCHED_AMOUNT']
        cumulative_written_off_amount = row['CUMULATIVE_WRITTEN_OFF_AMOUNT']
        prin_ln_waived_during_curr_qtr = row['PRIN_LN_WAIVED_DURING_CURR_QTR']
        inst_ln_waived_during_curr_qtr = row['INST_LN_WAIVED_DURING_CURR_QTR']
        prin_ln_writt_during_curr_qtr = row['PRIN_LN_WRITT_DURING_CURR_QTR']
        inst_ln_writt_during_curr_qtr = row['INST_LN_WRITT_DURING_CURR_QTR']
        r_agt_wrt_off_ln_dur_curr_qtr = row['R_AGT_WRT_OFF_LN_DUR_CURR_QTR']
        other_rcy_agt_classified_ln = row['OTHER_RCY_AGT_CLASSIFIED_LN']
        rit = ExtTPsQLnrecRecovery(
            dated=date_id,
            fi_id=fi_id,
            ps_coa=ps_coa,
            product_type_id=product_type_id,
            loan_class_id=loan_class_id,
            remarks=remarks,
            loan_amt_bdt=loan_amt_bdt,
            written_off_amount=written_off_amount,
            cash_recovery=cash_recovery,
            new_classified_advance=new_classified_advance,
            resched_amount=resched_amount,
            cumulative_written_off_amount=cumulative_written_off_amount,
            prin_ln_waived_during_curr_qtr=prin_ln_waived_during_curr_qtr,
            inst_ln_waived_during_curr_qtr=inst_ln_waived_during_curr_qtr,
            prin_ln_writt_during_curr_qtr=prin_ln_writt_during_curr_qtr,
            inst_ln_writt_during_curr_qtr=inst_ln_writt_during_curr_qtr,
            r_agt_wrt_off_ln_dur_curr_qtr=r_agt_wrt_off_ln_dur_curr_qtr,
            other_rcy_agt_classified_ln=other_rcy_agt_classified_ln,
        )
        objs.append(rit)
    try:
        ExtTPsQLnrecRecovery.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsQLnrecRecovery.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_q_sh_dir_info(id, db, meta):
    job = "insert_rit_t_ps_q_sh_dir_info"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsQShDirInfo.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI NAME']
        director_name = row["DIRECTOR'S NAME"]
        designation = row['DESIGNATION']
        dob = row['DATE OF BIRTH']
        nid = row['NATIONAL ID NO']
        tin = row['TAX ID NUMBER']
        passport_no = row['PASSPORT NO']
        fname = row["FATHER'S NAME"]
        mname = row["MOTHER'S NAME"]
        sname = row['SPOUSE NAME']
        present_address = row['PRESENT ADDRESS']
        permanent_address = row['PERMANENT ADDRESS']
        educational_qualification = row['EDUCATIONAL QUALIFICATION']
        work_experience = row['WORKING EXPERIENCE (IN YEARS)']
        date_of_first_appointment = row['DATE OF FIRST APPOINTMENT']
        date_of_last_app_or_reapp = row['DATE OF LAST APPOINTMENT/REAPPOINTMENT']
        interval_bet_subsequent_app = row['INTERVAL(S)  BETWEEN EACH SUBSEQUENT APPOINTMENT']
        fi_paid_up_capital = row["FI'S PAID UP CAPITAL"]
        no_of_shares_own = row['NO. OF SHARES(OWN)']
        total_no_of_shares = row['TOTAL NO. OF SHARES(OWN & FAMILY)']
        total_face_value_shareholdings = row['TOTAL FACE VALUE OF SHAREHOLDINGS(in TK)']
        nominating_shareholder_name = row["NOMINATING SHAREHOLDER'S (INSTITUTION) NAME"]
        total_value_of_nm_holdings = row["TOTAL FACE VALUE OF NOMINATING INSTITUTION'S SHAREHOLDINGS"]
        meeting_held = row['MEETING HELD']
        meeting_attended = row['MEETING ATTENDED']
        remarks = row['REMARKS']
        freq_indicator = row['FREQ. INDICATOR']
        rit = ExtTPsQShDirInfo(
            dated=date_id,
            fi_id=fi_id,
            director_name=director_name,
            designation=designation,
            dob=dob,
            nid=nid,
            tin=tin,
            passport_no=passport_no,
            fname=fname,
            mname=mname,
            sname=sname,
            present_address=present_address,
            permanent_address=permanent_address,
            educational_qualification=educational_qualification,
            work_experience=work_experience,
            date_of_first_appointment=date_of_first_appointment,
            date_of_last_app_or_reapp=date_of_last_app_or_reapp,
            interval_bet_subsequent_app=interval_bet_subsequent_app,
            fi_paid_up_capital=fi_paid_up_capital,
            no_of_shares_own=no_of_shares_own,
            total_no_of_shares=total_no_of_shares,
            total_face_value_shareholdings=total_face_value_shareholdings,
            nominating_shareholder_name=nominating_shareholder_name,
            total_value_of_nm_holdings=total_value_of_nm_holdings,
            meeting_held=meeting_held,
            meeting_attended=meeting_attended,
            remarks=remarks,
            freq_indicator=freq_indicator,
        )
        objs.append(rit)
    try:
        ExtTPsQShDirInfo.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsQShDirInfo.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_q_bank_dir_loans(id, db, meta):
    job = "insert_rit_t_ps_q_bank_dir_loans"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsQBankDirLoans.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["FI_ID"]
        dir_fi_id = row["DIRECTOR'S_BANK"]
        collateral_id = row["COLLATERAL_ID"]
        borrower_name = row["BORROWER_NAME"]
        purpose = row["PURPOSE"]
        bb_sanction_no = row["BB_SANCTION_NO"]
        loan_class_id = row["LOAN_CLASS_ID"]
        product_type_id = row["PRODUCT_TYPE_ID"]
        dos_id = row["DOS_ID"]
        tax_identification_number = row["TAX_IDENTIFICATION_NUMBER"]
        nature_interest_code = row["NATURE_INTEREST_CODE"]
        remarks = row["REMARKS"]
        approval_date_of_loan = row["APPROVAL_DATE_OF_LOAN"]
        overdue_date_of_loan = row["OVERDUE_DATE_OF_LOAN"]
        default_date_of_loan = row["DEFAULT_DATE_OF_LOAN"]
        sanction_date = row["SANCTION_DATE"]
        validity_expiry_date = row["VALIDITY_EXPIRY_DATE"]
        bb_sanction_date = row["BB_SANCTION_DATE"]
        overdue_amount = row["OVERDUE_AMOUNT"]
        total_outstanding_amt = row["TOTAL_OUTSTANDING_AMT"]
        dir_funded_outs_amt = row["DIR_FUNDED_OUTS_AMT"]
        indir_non_funded_outs_amt = row["INDIR_NON-FUNDED_OUTS_AMT"]
        sanction_amount = row["SANCTION_AMOUNT"]
        security_value = row["SECURITY_VALUE"]
        default_amount = row["DEFAULT_AMOUNT"]
        perspective_code = row["PERSPECTIVE_CODE"]
        dir_borr_class = row["DIRECTOR'S BORROWER CLASSIFICATION"]
        remarks1 = row["REMARKS_1"]
        rit = ExtTPsQBankDirLoans(
            dated=date_id,
            fi_id=fi_id,
            dir_fi_id=dir_fi_id,
            collateral_id=collateral_id,
            borrower_name=borrower_name,
            purpose=purpose,
            bb_sanction_no=bb_sanction_no,
            loan_class_id=loan_class_id,
            product_type_id=product_type_id,
            dos_id=dos_id,
            tax_identification_number=tax_identification_number,
            nature_interest_code=nature_interest_code,
            remarks=remarks,
            approval_date_of_loan=approval_date_of_loan,
            overdue_date_of_loan=overdue_date_of_loan,
            default_date_of_loan=default_date_of_loan,
            sanction_date=sanction_date,
            validity_expiry_date=validity_expiry_date,
            bb_sanction_date=bb_sanction_date,
            overdue_amount=overdue_amount,
            total_outstanding_amt=total_outstanding_amt,
            dir_funded_outs_amt=dir_funded_outs_amt,
            indir_non_funded_outs_amt=indir_non_funded_outs_amt,
            sanction_amount=sanction_amount,
            security_value=security_value,
            default_amount=default_amount,
            perspective_code=perspective_code,
            dir_borr_class=dir_borr_class,
            remarks1=remarks1,
        )
        objs.append(rit)
    try:
        ExtTPsQBankDirLoans.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsQBankDirLoans.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_q_fi_dir_loans(id, db, meta):
    job = "insert_rit_t_ps_q_fi_dir_loans"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsQFiDirLoans.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["FI_ID"]
        dir_fi_id = row["DIRECTOR'S_FI"]
        collateral_id = row["COLLATERAL_ID"]
        borrower_name = row["BORROWER_NAME"]
        purpose = row["PURPOSE"]
        bb_sanction_no = row["BB_SANCTION_NO"]
        loan_class_id = row["LOAN_CLASS_ID"]
        product_type_id = row["PRODUCT_TYPE_ID"]
        dos_id = row["DOS_ID"]
        tax_identification_number = row["TAX_IDENTIFICATION_NUMBER"]
        nature_interest_code = row["NATURE_INTEREST_CODE"]
        remarks = row["REMARKS"]
        approval_date_of_loan = row["APPROVAL_DATE_OF_LOAN"]
        overdue_date_of_loan = row["OVERDUE_DATE_OF_LOAN"]
        default_date_of_loan = row["DEFAULT_DATE_OF_LOAN"]
        sanction_date = row["SANCTION_DATE"]
        validity_expiry_date = row["VALIDITY_EXPIRY_DATE"]
        bb_sanction_date = row["BB_SANCTION_DATE"]
        overdue_amount = row["OVERDUE_AMOUNT"]
        total_outstanding_amt = row["TOTAL_OUTSTANDING_AMT"]
        dir_funded_outs_amt = row["DIR_FUNDED_OUTS_AMT"]
        indir_non_funded_outs_amt = row["INDIR_NON-FUNDED_OUTS_AMT"]
        sanction_amount = row["SANCTION_AMOUNT"]
        security_value = row["SECURITY_VALUE"]
        default_amount = row["DEFAULT_AMOUNT"]
        perspective_code = row["PERSPECTIVE_CODE"]
        dir_borr_class = row["DIRECTOR'S BORROWER CLASSIFICATION"]
        remarks1 = row["REMARKS_1"]
        rit = ExtTPsQFiDirLoans(
            dated=date_id,
            fi_id=fi_id,
            dir_fi_id=dir_fi_id,
            collateral_id=collateral_id,
            borrower_name=borrower_name,
            purpose=purpose,
            bb_sanction_no=bb_sanction_no,
            loan_class_id=loan_class_id,
            product_type_id=product_type_id,
            dos_id=dos_id,
            tax_identification_number=tax_identification_number,
            nature_interest_code=nature_interest_code,
            remarks=remarks,
            approval_date_of_loan=approval_date_of_loan,
            overdue_date_of_loan=overdue_date_of_loan,
            default_date_of_loan=default_date_of_loan,
            sanction_date=sanction_date,
            validity_expiry_date=validity_expiry_date,
            bb_sanction_date=bb_sanction_date,
            overdue_amount=overdue_amount,
            total_outstanding_amt=total_outstanding_amt,
            dir_funded_outs_amt=dir_funded_outs_amt,
            indir_non_funded_outs_amt=indir_non_funded_outs_amt,
            sanction_amount=sanction_amount,
            security_value=security_value,
            default_amount=default_amount,
            perspective_code=perspective_code,
            dir_borr_class=dir_borr_class,
            remarks1=remarks1,
        )
        objs.append(rit)
    try:
        ExtTPsQFiDirLoans.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsQFiDirLoans.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_nbfi_monitor_br(id, db, meta):
    job = "insert_rit_t_ps_m_nbfi_monitor_br"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMFiMonitorBr.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["NBFI_ID"]
        fi_branch_id = row["BRANCH_ID"]
        ps_coa_id = row["SUPERVISION_COA_ID"]
        ps_coa_desc = row["COA_DESCRIPTION"]
        amount_bdt = row["AMOUNT_BDT"]
        islamic_conventional_ind = row["ISLAMIC-CONVENTIONAL INDICATOR"]
        office_ind = row["OFFICE_IND"]
        rit = ExtTPsMFiMonitorBr(
            dated=date_id,
            fi_id=fi_id,
            fi_branch_id=fi_branch_id,
            ps_coa_id=ps_coa_id,
            ps_coa_desc=ps_coa_desc,
            amount_bdt=amount_bdt,
            islamic_conventional_ind=islamic_conventional_ind,
            office_ind=office_ind
        )
        objs.append(rit)
    try:
        ExtTPsMFiMonitorBr.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMFiMonitorBr.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_nbfi_monitor_ho(id, db, meta):
    job = "insert_rit_t_ps_m_nbfi_monitor_ho"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMFiMonitorHo.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["NBFI_ID"]
        fi_branch_id = row["HO_ID"]
        ps_coa_id = row["SUPERVISION_COA_ID"]
        ps_coa_desc = row["COA_DESCRIPTION"]
        amount_bdt = row["AMOUNT_BDT"]
        islamic_conventional_ind = row["ISLAMIC-CONVENTIONAL INDICATOR"]
        office_ind = row["OFFICE_IND"]
        rit = ExtTPsMFiMonitorHo(
            dated=date_id,
            fi_id=fi_id,
            fi_branch_id=fi_branch_id,
            ps_coa_id=ps_coa_id,
            ps_coa_desc=ps_coa_desc,
            amount_bdt=amount_bdt,
            islamic_conventional_ind=islamic_conventional_ind,
            office_ind=office_ind
        )
        objs.append(rit)
    try:
        ExtTPsMFiMonitorHo.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMFiMonitorHo.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_q_basel_bsl3(id, db, meta):
    job = "insert_rit_t_ps_q_basel_bsl3"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsQBaselBsl3.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["FI_ID"]
        basel_coa = row["BASEL_COA"]
        amount_bdt = row["AMOUNT_BDT"]
        risk_weighted_assets = row["RISK_WEIGHTED_ASSETS"]
        amount_market_value = row["AMOUNT_MARKET_VALUE"]
        cost_price = row["COST_PRICE"]
        capital_charge = row["CAPITAL_CHARGE"]
        notional_amount = row["NOTIONAL_AMOUNT"]
        cr_exposure = row["CR_EXPOSURE"]
        ccf = row["CCF"]
        risk_weight = row["RISK_WEIGHT"]
        market_price = row["MARKET_PRICE"]
        solo_consolidation_position = row["SOLO_CONS_INDICATOR"]
        rit = ExtTPsQBaselBsl3(
            dated=date_id,
            fi_id=fi_id,
            basel_coa=basel_coa,
            amount_bdt=amount_bdt,
            risk_weighted_assets=risk_weighted_assets,
            amount_market_value=amount_market_value,
            cost_price=cost_price,
            capital_charge=capital_charge,
            notional_amount=notional_amount,
            cr_exposure=cr_exposure,
            ccf=ccf,
            risk_weight=risk_weight,
            market_price=market_price,
            solo_consolidation_position=solo_consolidation_position,
        )
        objs.append(rit)
    try:
        ExtTPsQBaselBsl3.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsQBaselBsl3.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_q_depo_cls_v2(id, db, meta):
    job = "insert_rit_t_me_q_depo_cls_v2"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeQDepoClsV2.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["FI_ID"]
        fi_branch_id = row["FI_BRANCH_ID"]
        account_number = row["ACCOUNT NUMBER"]
        gender_code = row["GENDER_CODE"]
        eco_sector_id = row["ECO_SECTOR_ID"]
        industry_scale_id = row["INDUSTRY_SCALE_ID"]
        product_type_id = row["PRODUCT_TYPE_ID"]
        interest_rate = row["INTEREST_RATE"]
        amount_bdt = row["AMOUNT_BDT"]
        rit = ExtTMeQDepoClsV2(
            dated=date_id,
            fi_id=fi_id,
            fi_branch_id=fi_branch_id,
            account_number=account_number,
            gender_code=gender_code,
            eco_sector_id=eco_sector_id,
            industry_scale_id=industry_scale_id,
            product_type_id=product_type_id,
            interest_rate=interest_rate,
            amount_bdt=amount_bdt,
        )
        objs.append(rit)
    try:
        ExtTMeQDepoClsV2.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeQDepoClsV2.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_liqdty_fi(id, db, meta):
    job = "insert_rit_t_ps_m_liqdty_fi"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMLiqdtyFi.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["FI_ID"]
        ps_coa_id = row["PS_COA"]
        aging_range = row["AGING_RANGE"]
        amount_bdt = row["AMOUNT_BDT"]
        rit = ExtTPsMLiqdtyFi(
            dated=date_id,
            fi_id=fi_id,
            ps_coa_id=ps_coa_id,
            aging_range=aging_range,
            amount_bdt=amount_bdt
        )
        objs.append(rit)
    try:
        ExtTPsMLiqdtyFi.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMLiqdtyFi.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_resched_loans(id, db, meta):
    job = "insert_rit_t_ps_m_resched_loans"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMReschedLoans.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["FI_ID"]
        loan_lease_recipient = row["LOAN LEASE RECIPIENT"]
        product_type_id = row["PRODUCT_TYPE_ID"]
        resched_step = row["RESCHED_STEP"]
        la_tl_no = row["ACCOUNT NUMBER"]
        remarks = row["REMARKS"]
        sanction_date = row["SANCTION_DATE"]
        overdue_date = row["OVERDUE_DATE"]
        reschedule_date = row["RESCHEDULE_DATE"]
        sanction_amount = row["SANCTION_AMOUNT"]
        overdue_amount = row["OVERDUE_AMOUNT"]
        down_payment = row["DOWN_PAYMENT"]
        percent_downpayment = row["PERCENT_DOWNPAYMENT"]
        amount_rescheduled = row["AMOUNT_RESCHEDULED"]
        outstanding_amount_bdt = row["OUTSTANDING_AMOUNT_BDT"]
        rit = ExtTPsMReschedLoans(
            dated=date_id,
            fi_id=fi_id,
            loan_lease_recipient=loan_lease_recipient,
            product_type_id=product_type_id,
            resched_step=resched_step,
            la_tl_no=la_tl_no,
            remarks=remarks,
            sanction_date=sanction_date,
            overdue_date=overdue_date,
            reschedule_date=reschedule_date,
            sanction_amount=sanction_amount,
            overdue_amount=overdue_amount,
            down_payment=down_payment,
            percent_downpayment=percent_downpayment,
            amount_rescheduled=amount_rescheduled,
            outstanding_amount_bdt=outstanding_amount_bdt
        )
        objs.append(rit)
    try:
        ExtTPsMReschedLoans.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMReschedLoans.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_slr_crr(id, db, meta):
    job = "insert_rit_t_ps_m_slr_crr"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMSlrCrr.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["FI_NAME"]
        product_type_id = row["PRODUCT_TYPE_ID"]
        ps_coa = row["PS_COA"]
        maintain_month = row["MAINTAIN_MONTH"]
        base_month = row["BASE_MONTH"]
        w1_balance = row["W1_BALANCE"]
        w2_balance = row["W2_BALANCE"]
        w3_balance = row["W3_BALANCE"]
        w4_balance = row["W4_BALANCE"]
        w5_balance = row["W5_BALANCE"]
        rit = ExtTPsMSlrCrr(
            dated=date_id,
            fi_id=fi_id,
            product_type_id=product_type_id,
            ps_coa=ps_coa,
            maintain_month=maintain_month,
            base_month=base_month,
            w1_balance=w1_balance,
            w2_balance=w2_balance,
            w3_balance=w3_balance,
            w4_balance=w4_balance,
            w5_balance=w5_balance,
        )
        objs.append(rit)
    try:
        ExtTPsMSlrCrr.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMSlrCrr.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_write_off_loanlease(id, db, meta):
    job = "insert_rit_t_ps_m_write_off_loanlease"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMWriteOffLoanlease.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["FI_NAME"]
        lessee_loan = row["LESSEE_LOAN"]
        account_number = row["ACCOUNT_NUMBER"]
        nature_of_loan_lease = row["Product_Type_ID"]
        board_approval_no = row["BOARD_APPROVAL_NO"]
        remarks = row["REMARKS"]
        legal_action_taken = row["LEGAL_ACTION_TAKEN"]
        prosecution_no = row["PROSECUTION_NO"]
        sanction_date = row["SANCTION_DATE"]
        bad_loan_date = row["BAD_LOAN_DATE"]
        prosecution_date = row["PROSECUTION_DATE"]
        written_off_date = row["WRITTEN_OFF_DATE"]
        approval_date = row["APPROVAL_DATE"]
        provision_amount = row["PROVISION_AMOUNT"]
        written_off_amount = row["WRITTEN_OFF_AMOUNT"]
        sanction_amount = row["SANCTION_AMOUNT"]
        outstanding_amount = row["OUTSTANDING_AMOUNT"]
        bad_loan_amount = row["BAD_LOAN_AMOUNT"]
        rit = ExtTPsMWriteOffLoanlease(
            dated=date_id,
            fi_id=fi_id,
            lessee_loan=lessee_loan,
            account_number=account_number,
            nature_of_loan_lease=nature_of_loan_lease,
            board_approval_no=board_approval_no,
            remarks=remarks,
            legal_action_taken=legal_action_taken,
            prosecution_no=prosecution_no,
            sanction_date=sanction_date,
            bad_loan_date=bad_loan_date,
            prosecution_date=prosecution_date,
            written_off_date=written_off_date,
            approval_date=approval_date,
            provision_amount=provision_amount,
            written_off_amount=written_off_amount,
            sanction_amount=sanction_amount,
            outstanding_amount=outstanding_amount,
            bad_loan_amount=bad_loan_amount,
        )
        objs.append(rit)
    try:
        ExtTPsMWriteOffLoanlease.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMWriteOffLoanlease.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_m_inr_non_res(id, db, meta):
    job = "insert_rit_t_me_m_inr_non_res"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 2, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeMInrNonRes.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        ccy_id = row["CCY_ID"]
        fi_id = row["FI_ID"]
        product_type_id = row["PRODUCT_TYPE_ID"]
        interest_rate = row["INTEREST RATE"]
        reporting_period = row["REPORTING PERIOD"]
        rit = ExtTMeMInrNonRes(
            dated=date_id,
            ccy_id=ccy_id,
            fi_id=fi_id,
            product_type_id=product_type_id,
            interest_rate=interest_rate,
            reporting_period=reporting_period
        )
        objs.append(rit)
    try:
        ExtTMeMInrNonRes.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeMInrNonRes.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_me_q_lted_transaction(id, db, meta):
    job = "insert_rit_t_me_q_lted_transaction"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 2, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTMeQLtedTransaction.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        serial = row["Serial"]
        fi_id = row["FI Name"]
        debtor_id = row["Debtor Name"]
        loan_id = row["Loan ID"]
        tranche_no = row["Tranche No."]
        currency_id = row["Tranche Currency"]
        loan_amount = row["Loan Amount"]
        agr_loan_con_date = row["Agreement Signing / Loan Contract Date"]
        opening_position = row["Opening Position"]
        transaction_type = row["Transaction Type"]
        t_date = row["Date"]
        amount = row["Amount"]
        closing_position = row["Closing Position"]
        loan_status = row["Loan Status"]
        rit = ExtTMeQLtedTransaction(
            dated=date_id,
            serial=serial,
            fi_id=fi_id,
            debtor_id=debtor_id,
            loan_id=loan_id,
            tranche_no=tranche_no,
            currency_id=currency_id,
            loan_amount=loan_amount,
            agr_loan_con_date=agr_loan_con_date,
            opening_position=opening_position,
            transaction_type=transaction_type,
            t_date=t_date,
            amount=amount,
            closing_position=closing_position,
            loan_status=loan_status,
        )
        objs.append(rit)
    try:
        ExtTMeQLtedTransaction.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTMeQLtedTransaction.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_fi_monitor_br(id, db, meta):
    job = "insert_rit_t_ps_m_fi_monitor_br"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMFiMonitorBr.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["BANK_ID"]
        fi_branch_id = row["BRANCH_ID"]
        ps_coa_id = row["SUPERVISION_COA_ID"]
        ps_coa_desc = row["COA_DESCRIPTION"]
        amount_bdt = row["AMOUNT_BDT"]
        islamic_conventional_ind = row["ISLAMIC-CONVENTIONAL INDICATOR"]
        office_ind = row["OFFICE_IND"]
        rit = ExtTPsMFiMonitorBr(
            dated=date_id,
            fi_id=fi_id,
            fi_branch_id=fi_branch_id,
            ps_coa_id=ps_coa_id,
            ps_coa_desc=ps_coa_desc,
            amount_bdt=amount_bdt,
            islamic_conventional_ind=islamic_conventional_ind,
            office_ind=office_ind
        )
        objs.append(rit)
    try:
        ExtTPsMFiMonitorBr.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMFiMonitorBr.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }


@shared_task
def insert_rit_t_ps_m_fi_monitor_ho(id, db, meta):
    job = "insert_rit_t_ps_m_fi_monitor_ho"
    decoded_list, status = get_decoded_list(id)
    if not status["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], status["msg"])
        return {
            "success": False,
            "msg": status["msg"]
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], fi_reporting_date["msg"])
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    try:
        refresh = ExtTPsMFiMonitorHo.objects.using(db).filter(dated=date_id, fi_id=fi)
        if refresh.using(db).exists():
            refresh.using(db).delete()
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FILTER_ERROR"])
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row["BANK_ID"]
        fi_branch_id = row["HO_ID"]
        ps_coa_id = row["SUPERVISION_COA_ID"]
        ps_coa_desc = row["COA_DESCRIPTION"]
        amount_bdt = row["AMOUNT_BDT"]
        islamic_conventional_ind = row["ISLAMIC-CONVENTIONAL INDICATOR"]
        office_ind = row["OFFICE_IND"]
        rit = ExtTPsMFiMonitorHo(
            dated=date_id,
            fi_id=fi_id,
            fi_branch_id=fi_branch_id,
            ps_coa_id=ps_coa_id,
            ps_coa_desc=ps_coa_desc,
            amount_bdt=amount_bdt,
            islamic_conventional_ind=islamic_conventional_ind,
            office_ind=office_ind
        )
        objs.append(rit)
    try:
        ExtTPsMFiMonitorHo.objects.using(db).bulk_create(objs)
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["FAILURE"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }
    try:
        count = ExtTPsMFiMonitorHo.objects.using(db).filter(dated=date_id, fi_id=fi).count()
        insert_rit_load_status(meta, job, MESSAGE["STATUS_SUCCESS"], MESSAGE["SUCCESS"], count)
        return {
                "success": True,
                "count": count,
                "msg": MESSAGE["SUCCESS"],
        }
    except:
        insert_rit_load_status(meta, job, MESSAGE["STATUS_FAILURE"], MESSAGE["COUNT_ERROR"])
        return {
            "success": False,
            "msg": MESSAGE["FAILURE"],
        }

