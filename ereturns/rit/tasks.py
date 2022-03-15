from celery import shared_task


import csv
from datetime import datetime

from ereturns.rit.models.models import RitSupervision
from ereturns.rit.models.rit_management_models import (
    DDates, StgTMeDFrxEchPos, StgTPsDLoanSpResSt, StgTMeMAssLiabSuppSbs, StgTMeMAssLiabObu, StgTMeMAssLiabFin,
    StgTMeMAssLiabBank
)

# from celery import current_app
# current_app.conf.CELERY_ALWAYS_EAGER = True
# current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


def get_decoded_list(id):
    file = RitSupervision.objects.get(id=id).file
    decoded_file_string = file.read().decode('utf-8')
    decoded_file = decoded_file_string.splitlines()
    return decoded_file


def get_fi_reporting_date(decoded_list, fi_index, db):
    reporting_date = decoded_list[2].split(",")[0]
    fi = int(decoded_list[2].split(",")[fi_index])
    date_id = None
    try:
        formated_date = datetime.strptime(reporting_date, "%d-%b-%y").date()
        date_id = DDates.objects.using(db).get(cal_date=formated_date).date_id
    except DDates.DoesNotExist:
        return {
            "success": False,
            "msg": "date_id does not exists."
        }
    return {
            "success": True,
            "date": date_id,
            "fi": fi,
    }


@shared_task
def insert_rit_t_me_d_frx_ech_pos(id, db):
    decoded_list = get_decoded_list(id)
    if not decoded_list:
        return {
            "success": False,
            "msg": "Empty file."
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 2, db)
    if not fi_reporting_date["success"]:
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    refresh = StgTMeDFrxEchPos.objects.using(db).filter(date_id=date_id, fi_id=fi)
    if refresh.using(db).exists():
        refresh.using('rit_mngt').delete()
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        ccy_id = row['CCY_ID']
        fi_id = row['FI_ID']
        me_coa = row['ME_COA']
        amount_fcy = 0 if row['AMOUNT'] == "" else row['AMOUNT']
        exchange_rate = row['EXCHANGE_RATE']
        open_position_limit = row['Open_Position_Limit']
        valid_ind = 1
        rit = StgTMeDFrxEchPos(date_id=date_id, ccy_id=ccy_id, fi_id=fi_id, monetary_coa_id=me_coa,
                               amount_fcy=amount_fcy, exchange_rate=exchange_rate,
                               open_position_limit=open_position_limit, valid_ind=valid_ind)
        objs.append(rit)
    StgTMeDFrxEchPos.objects.using(db).bulk_create(objs)
    count = StgTMeDFrxEchPos.objects.using(db).filter(date_id=date_id, fi_id=fi).count()
    return {
            "success": True,
            "count": count,
            "msg": "Data inserted successfully.",
    }


@shared_task
def insert_rit_t_ps_d_loan_sp_res_st(id, db):
    decoded_list = get_decoded_list(id)
    if not decoded_list:
        return {
            "success": False,
            "msg": "Empty file."
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    refresh = StgTPsDLoanSpResSt.objects.using(db).filter(date_id=date_id, fi_id=fi)
    if refresh.using(db).exists():
        refresh.using(db).delete()
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
        rit = StgTPsDLoanSpResSt(date_id=date_id, fi_id=fi_id, facility_type=facility_type,
                                 application_no=application_no, application_approved=application_approved,
                                 outstanding_amount=outstanding_amount, down_payment_amount=down_payment_amount,
                                 interest_suspense=interest_suspense, unapplied_interest=unapplied_interest,
                                 interest_waived=interest_waived, amount_rescheduled_exit=amount_rescheduled_exit)
        objs.append(rit)
    StgTPsDLoanSpResSt.objects.using(db).bulk_create(objs)
    count = StgTPsDLoanSpResSt.objects.using(db).filter(date_id=date_id, fi_id=fi).count()
    return {
            "success": True,
            "count": count,
            "msg": "Data inserted successfully.",
    }


@shared_task
def insert_rit_t_me_m_ass_liab_supp_sbs(id, db):
    decoded_list = get_decoded_list(id)
    if not decoded_list:
        return {
            "success": False,
            "msg": "Empty file."
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    refresh = StgTMeMAssLiabSuppSbs.objects.using(db).filter(date_id=date_id, fi_id=fi)
    if refresh.using(db).exists():
        refresh.using(db).delete()
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        me_coa = row['ME_COA']
        amount_bdt = row['AMOUNT BDT']
        rit = StgTMeMAssLiabSuppSbs(date_id=date_id, fi_id=fi_id, monetary_coa_id=me_coa, amount_bdt=amount_bdt)
        objs.append(rit)
    StgTMeMAssLiabSuppSbs.objects.using(db).bulk_create(objs)
    count = StgTMeMAssLiabSuppSbs.objects.using(db).filter(date_id=date_id, fi_id=fi).count()
    return {
            "success": True,
            "count": count,
            "msg": "Data inserted successfully.",
    }


@shared_task
def insert_rit_t_me_m_ass_liab_obu(id, db):
    decoded_list = get_decoded_list(id)
    if not decoded_list:
        return {
            "success": False,
            "msg": "Empty file."
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    refresh = StgTMeMAssLiabObu.objects.using(db).filter(date_id=date_id, fi_id=fi)
    if refresh.using(db).exists():
        refresh.using(db).delete()
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        me_coa = row['ME_COA']
        amount_bdt = row['AMOUNT BDT']
        rit = StgTMeMAssLiabObu(date_id=date_id, fi_id=fi_id, monetary_coa_id=me_coa, amount_bdt=amount_bdt)
        objs.append(rit)
    StgTMeMAssLiabObu.objects.using(db).bulk_create(objs)
    count = StgTMeMAssLiabObu.objects.using(db).filter(date_id=date_id, fi_id=fi).count()
    return {
            "success": True,
            "count": count,
            "msg": "Data inserted successfully.",
    }


@shared_task
def insert_rit_t_me_m_ass_liab_fin(id, db):
    decoded_list = get_decoded_list(id)
    if not decoded_list:
        return {
            "success": False,
            "msg": "Empty file."
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    refresh = StgTMeMAssLiabFin.objects.using(db).filter(date_id=date_id, fi_id=fi)
    if refresh.using(db).exists():
        refresh.using(db).delete()
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        me_coa = row['ME_COA']
        amount_bdt = row['AMOUNT BDT']
        rit = StgTMeMAssLiabFin(date_id=date_id, fi_id=fi_id, monetary_coa_id=me_coa, amount_bdt=amount_bdt)
        objs.append(rit)
    StgTMeMAssLiabFin.objects.using(db).bulk_create(objs)
    count = StgTMeMAssLiabFin.objects.using(db).filter(date_id=date_id, fi_id=fi).count()
    return {
            "success": True,
            "count": count,
            "msg": "Data inserted successfully.",
    }


@shared_task
def insert_rit_t_me_m_ass_liab_bank(id, db):
    decoded_list = get_decoded_list(id)
    if not decoded_list:
        return {
            "success": False,
            "msg": "Empty file."
        }
    fi_reporting_date = get_fi_reporting_date(decoded_list, 1, db)
    if not fi_reporting_date["success"]:
        return fi_reporting_date
    date_id = fi_reporting_date["date"]
    fi = fi_reporting_date["fi"]
    refresh = StgTMeMAssLiabBank.objects.using(db).filter(date_id=date_id, fi_id=fi)
    if refresh.using(db).exists():
        refresh.using(db).delete()
    reader = csv.DictReader(decoded_list[1:])
    objs = []
    for row in reader:
        fi_id = row['FI_NAME']
        me_coa = row['ME_COA']
        amount_bdt = row['AMOUNT BDT']
        rit = StgTMeMAssLiabBank(date_id=date_id, fi_id=fi_id, monetary_coa_id=me_coa, amount_bdt=amount_bdt)
        objs.append(rit)
    StgTMeMAssLiabBank.objects.using(db).bulk_create(objs)
    count = StgTMeMAssLiabBank.objects.using(db).filter(date_id=date_id, fi_id=fi).count()
    return {
            "success": True,
            "count": count,
            "msg": "Data inserted successfully.",
    }
