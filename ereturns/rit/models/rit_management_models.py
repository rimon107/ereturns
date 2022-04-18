# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DDates(models.Model):
    date_id = models.BigIntegerField(primary_key=True)
    cal_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_dates'


class ExtTMeDFrxEchPos(models.Model):
    dated = models.CharField(max_length=20, blank=True, null=True)
    ccy_id = models.CharField(max_length=25, blank=True, null=True)
    fi_id = models.CharField(max_length=25, blank=True, null=True)
    me_coa = models.CharField(max_length=25, blank=True, null=True)
    amount = models.CharField(max_length=25, blank=True, null=True)
    exchange_rate = models.CharField(max_length=25, blank=True, null=True)
    open_position_limit = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_d_frx_ech_pos'


class ExtTMeDRemittance(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    serial_no = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    rep_type = models.CharField(max_length=255, blank=True, null=True)
    sched_code = models.CharField(max_length=255, blank=True, null=True)
    type_code = models.CharField(max_length=255, blank=True, null=True)
    payrec_purpose_id = models.CharField(max_length=255, blank=True, null=True)
    ccy_id = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.CharField(max_length=255, blank=True, null=True)
    district_id = models.CharField(max_length=255, blank=True, null=True)
    nid = models.CharField(max_length=255, blank=True, null=True)
    passport = models.CharField(max_length=255, blank=True, null=True)
    amount_fcy = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_d_remittance'


class ExtTMeMAssFor(models.Model):
    dated = models.CharField(max_length=20, blank=True, null=True)
    fi_id = models.CharField(max_length=25, blank=True, null=True)
    ccy_id = models.CharField(max_length=25, blank=True, null=True)
    exchange_rate = models.CharField(max_length=25, blank=True, null=True)
    amount_bdt = models.CharField(max_length=25, blank=True, null=True)
    monetary_coa_id = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_ass_for'


class ExtTMeMAssForObu(models.Model):
    dated = models.CharField(max_length=20, blank=True, null=True)
    fi_id = models.CharField(max_length=25, blank=True, null=True)
    ccy_id = models.CharField(max_length=25, blank=True, null=True)
    exchange_rate = models.CharField(max_length=25, blank=True, null=True)
    amount_bdt = models.CharField(max_length=25, blank=True, null=True)
    monetary_coa_id = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_ass_for_obu'


class ExtTMeMAssLiab(models.Model):
    dated = models.CharField(max_length=20, blank=True, null=True)
    fi_id = models.CharField(max_length=25, blank=True, null=True)
    me_coa = models.CharField(max_length=25, blank=True, null=True)
    amount_bdt = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_ass_liab'


class ExtTMeMAssLiabObu(models.Model):
    dated = models.CharField(max_length=20, blank=True, null=True)
    fi_id = models.CharField(max_length=25, blank=True, null=True)
    me_coa = models.CharField(max_length=25, blank=True, null=True)
    amount_bdt = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_ass_liab_obu'


class ExtTMeMAssLiabSuppSbs(models.Model):
    dated = models.CharField(max_length=20, blank=True, null=True)
    fi_id = models.CharField(max_length=25, blank=True, null=True)
    monetary_coa_id = models.CharField(max_length=25, blank=True, null=True)
    amount_bdt = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_ass_liab_supp_sbs'


class ExtTMeMDepoDri(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    balance_bdt = models.CharField(max_length=255, blank=True, null=True)
    interest_rate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_depo_dri'


class ExtTMeMEbankingEcommerce(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    coa_id = models.CharField(max_length=255, blank=True, null=True)
    data_in_number = models.CharField(max_length=255, blank=True, null=True)
    data_in_text = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_ebanking_ecommerce'


class ExtTMeMFrcTrn(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    ccy_id = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    payrec_purpose_id = models.CharField(max_length=255, blank=True, null=True)
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True)
    importer_exporter = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    encashment_no_company_name = models.CharField(max_length=255, blank=True, null=True)
    amount_fcy = models.CharField(max_length=255, blank=True, null=True)
    quantity_volume = models.CharField(max_length=255, blank=True, null=True)
    transaction_count = models.CharField(max_length=255, blank=True, null=True)
    encashment_date = models.CharField(max_length=255, blank=True, null=True)
    transaction_date = models.CharField(max_length=255, blank=True, null=True)
    serial_no = models.CharField(max_length=255, blank=True, null=True)
    rep_type = models.CharField(max_length=255, blank=True, null=True)
    sched_code = models.CharField(max_length=255, blank=True, null=True)
    type_code = models.CharField(max_length=255, blank=True, null=True)
    commodity_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_frc_trn'


class ExtTMeMFrcTrnSupp(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    serial_no = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    rep_type = models.CharField(max_length=255, blank=True, null=True)
    sched_code = models.CharField(max_length=255, blank=True, null=True)
    type_code = models.CharField(max_length=255, blank=True, null=True)
    ccy_id = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.CharField(max_length=255, blank=True, null=True)
    encashment_no_company_name = models.CharField(max_length=255, blank=True, null=True)
    encashment_date = models.CharField(max_length=255, blank=True, null=True)
    importer_exporter = models.CharField(max_length=255, blank=True, null=True)
    transaction_date = models.CharField(max_length=255, blank=True, null=True)
    amount_fcy = models.CharField(max_length=255, blank=True, null=True)
    exchange_rate = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_frc_trn_supp'


class ExtTMeMInrNonRes(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    ccy_id = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    interest_rate = models.CharField(max_length=255, blank=True, null=True)
    reporting_period = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_inr_non_res'


class ExtTMeMLnaDl(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    eco_purpose_id = models.CharField(max_length=255, blank=True, null=True)
    prev_outstanding_amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    cur_actual_amount_disbursed = models.CharField(max_length=255, blank=True, null=True)
    cur_interest_amount = models.CharField(max_length=255, blank=True, null=True)
    cur_recovered_amount = models.CharField(max_length=255, blank=True, null=True)
    written_off_amount = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_lna_dl'


class ExtTMeMLnaDlObu(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    eco_purpose_id = models.CharField(max_length=255, blank=True, null=True)
    prev_outstanding_amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    cur_actual_amount_disbursed = models.CharField(max_length=255, blank=True, null=True)
    cur_interest_amount = models.CharField(max_length=255, blank=True, null=True)
    cur_recovered_amount = models.CharField(max_length=255, blank=True, null=True)
    written_off_amount = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_lna_dl_obu'


class ExtTMeMLnaRates(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    interest_rate = models.CharField(max_length=255, blank=True, null=True)
    advances_bdt = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_lna_rates'


class ExtTMeMPortInv(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    instrument_type_code = models.CharField(max_length=255, blank=True, null=True)
    opening_position_amount = models.CharField(max_length=255, blank=True, null=True)
    purchase_amount = models.CharField(max_length=255, blank=True, null=True)
    sale_amount = models.CharField(max_length=255, blank=True, null=True)
    gain_loss = models.CharField(max_length=255, blank=True, null=True)
    closing_position = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    investor_id = models.CharField(max_length=255, blank=True, null=True)
    security_code = models.CharField(max_length=255, blank=True, null=True)
    economic_sector = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_port_inv'


class ExtTMeMPortSurvey(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    investor_id = models.CharField(max_length=255, blank=True, null=True)
    nita_coa = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_port_survey'


class ExtTMeMSted(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    serial_no = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    debtor_name = models.CharField(max_length=255, blank=True, null=True)
    instrument_classification = models.CharField(max_length=255, blank=True, null=True)
    tradable_item = models.CharField(max_length=255, blank=True, null=True)
    creditor_name = models.CharField(max_length=255, blank=True, null=True)
    creditor_type = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.CharField(max_length=255, blank=True, null=True)
    all_cost_percent_annum = models.CharField(max_length=255, blank=True, null=True)
    interest_rate = models.CharField(max_length=255, blank=True, null=True)
    currency_id = models.CharField(max_length=255, blank=True, null=True)
    total_borrowing_amount = models.CharField(max_length=255, blank=True, null=True)
    f_drawing_disb_date = models.CharField(max_length=255, blank=True, null=True)
    l_principal_pay_date = models.CharField(max_length=255, blank=True, null=True)
    maturity_in_days = models.CharField(max_length=255, blank=True, null=True)
    opening_pos_principal_outs = models.CharField(max_length=255, blank=True, null=True)
    amount_drawn_during_rep_mon = models.CharField(max_length=255, blank=True, null=True)
    principal_paid_dur_rep_mon = models.CharField(max_length=255, blank=True, null=True)
    interest_paid_dur_rep_mon = models.CharField(max_length=255, blank=True, null=True)
    others_fees_rep_mon = models.CharField(max_length=255, blank=True, null=True)
    overdue_amount = models.CharField(max_length=255, blank=True, null=True)
    closing_position = models.CharField(max_length=255, blank=True, null=True)
    lc_no = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_m_sted'


class ExtTMeQAcep(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    purpose_type_id = models.CharField(max_length=255, blank=True, null=True)
    economic_sector_id = models.CharField(max_length=255, blank=True, null=True)
    sanction_limit = models.CharField(max_length=255, blank=True, null=True)
    disbursement_amount = models.CharField(max_length=255, blank=True, null=True)
    recovery_amount = models.CharField(max_length=255, blank=True, null=True)
    classified_amount_ss = models.CharField(max_length=255, blank=True, null=True)
    classified_amount_df = models.CharField(max_length=255, blank=True, null=True)
    classified_amount_b_l = models.CharField(max_length=255, blank=True, null=True)
    unclassified_amount_sma = models.CharField(max_length=255, blank=True, null=True)
    unclassified_amount_std = models.CharField(max_length=255, blank=True, null=True)
    overdue_amount = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_q_acep'


class ExtTMeQDepoClsV2(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    gender_code = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    industry_scale_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    interest_rate = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_q_depo_cls_v2'


class ExtTMeQInvForFi1(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_name = models.CharField(max_length=255, blank=True, null=True)
    investor_channel = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    legal_enterprise = models.CharField(max_length=255, blank=True, null=True)
    enterprise_type = models.CharField(max_length=255, blank=True, null=True)
    enterprise_location = models.CharField(max_length=255, blank=True, null=True)
    sector_major_activities = models.CharField(max_length=255, blank=True, null=True)
    date_incorporation_reg = models.CharField(max_length=255, blank=True, null=True)
    date_of_imp = models.CharField(max_length=255, blank=True, null=True)
    fellow_enterprise = models.CharField(max_length=255, blank=True, null=True)
    location_fellow_ent = models.CharField(max_length=255, blank=True, null=True)
    location_common_parent = models.CharField(max_length=255, blank=True, null=True)
    investor_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    percentage_equity_share = models.CharField(max_length=255, blank=True, null=True)
    total_foreign_inv_bdt = models.CharField(max_length=255, blank=True, null=True)
    total_external_debt = models.CharField(max_length=255, blank=True, null=True)
    total_paid_up = models.CharField(max_length=255, blank=True, null=True)
    import_date = models.CharField(max_length=255, blank=True, null=True)
    imported_by = models.CharField(max_length=255, blank=True, null=True)
    imp_amount = models.CharField(max_length=255, blank=True, null=True)
    capital_contribution = models.CharField(max_length=255, blank=True, null=True)
    number_foreign_employee = models.CharField(max_length=255, blank=True, null=True)
    num_local_employee = models.CharField(max_length=255, blank=True, null=True)
    other_bank = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_q_inv_for_fi_1'


class ExtTMeQInvForFi2(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_name = models.CharField(max_length=255, blank=True, null=True)
    investor_channel = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    sector_major_activities = models.CharField(max_length=255, blank=True, null=True)
    legal_enterprise = models.CharField(max_length=255, blank=True, null=True)
    date_of_imp = models.CharField(max_length=255, blank=True, null=True)
    location_ent = models.CharField(max_length=255, blank=True, null=True)
    total_paid_up = models.CharField(max_length=255, blank=True, null=True)
    name_invst_ent_abroad = models.CharField(max_length=255, blank=True, null=True)
    country_invst_ent_abroad = models.CharField(max_length=255, blank=True, null=True)
    percentage_equity_share = models.CharField(max_length=255, blank=True, null=True)
    legal_form_invst_ent_abroad = models.CharField(max_length=255, blank=True, null=True)
    sect_maj_act_invst_ent_abrd = models.CharField(max_length=255, blank=True, null=True)
    date_of_imp_invst_ent_abroad = models.CharField(max_length=255, blank=True, null=True)
    tot_equity_invst_abrd_amount = models.CharField(max_length=255, blank=True, null=True)
    tot_paid_up_invst_ent_abrd = models.CharField(max_length=255, blank=True, null=True)
    fellow_enterprise = models.CharField(max_length=255, blank=True, null=True)
    location_fellow_enterprise = models.CharField(max_length=255, blank=True, null=True)
    location_common_parent = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_q_inv_for_fi_2'


class ExtTMeQInvNonResFi(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    investor_channel = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    enterprise_type = models.CharField(max_length=255, blank=True, null=True)
    sector_major_activities = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    mecoa_code = models.CharField(max_length=255, blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)
    opening_position_date = models.CharField(max_length=255, blank=True, null=True)
    opening_position = models.CharField(max_length=255, blank=True, null=True)
    position_increase = models.CharField(max_length=255, blank=True, null=True)
    position_decrease = models.CharField(max_length=255, blank=True, null=True)
    changes_due_to_exchange_rate = models.CharField(max_length=255, blank=True, null=True)
    changes_due_to_price_change = models.CharField(max_length=255, blank=True, null=True)
    change_due_to_others = models.CharField(max_length=255, blank=True, null=True)
    closing_position_reported = models.CharField(max_length=255, blank=True, null=True)
    closing_position_calculated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_q_inv_non_res_fi'


class ExtTMeQLnaV2(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    gender_code = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    eco_purpose_id = models.CharField(max_length=255, blank=True, null=True)
    industry_scale_id = models.CharField(max_length=255, blank=True, null=True)
    collateral_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    loan_class_id = models.CharField(max_length=255, blank=True, null=True)
    interest_rate = models.CharField(max_length=255, blank=True, null=True)
    sanction_amount = models.CharField(max_length=255, blank=True, null=True)
    opening_balance = models.CharField(max_length=255, blank=True, null=True)
    disbursed_amount = models.CharField(max_length=255, blank=True, null=True)
    recovered_amount = models.CharField(max_length=255, blank=True, null=True)
    accrued_interest = models.CharField(max_length=255, blank=True, null=True)
    other_charges = models.CharField(max_length=255, blank=True, null=True)
    adjustment_amount = models.CharField(max_length=255, blank=True, null=True)
    write_off_amount = models.CharField(max_length=255, blank=True, null=True)
    outstanding_amount = models.CharField(max_length=255, blank=True, null=True)
    overdue_amount = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_q_lna_v2'


class ExtTMeQLtedTransaction(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    serial = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    debtor_id = models.CharField(max_length=255, blank=True, null=True)
    loan_id = models.CharField(max_length=255, blank=True, null=True)
    tranche_no = models.CharField(max_length=255, blank=True, null=True)
    currency_id = models.CharField(max_length=255, blank=True, null=True)
    loan_amount = models.CharField(max_length=255, blank=True, null=True)
    agr_loan_con_date = models.CharField(max_length=255, blank=True, null=True)
    opening_position = models.CharField(max_length=255, blank=True, null=True)
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    t_date = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    closing_position = models.CharField(max_length=255, blank=True, null=True)
    loan_status = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_q_lted_transaction'


class ExtTMeQSmeLoan(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    sme_category = models.CharField(max_length=255, blank=True, null=True)
    sub_sector = models.CharField(max_length=255, blank=True, null=True)
    ln_segregation = models.CharField(max_length=255, blank=True, null=True)
    nature_of_enterprise = models.CharField(max_length=255, blank=True, null=True)
    number_of_enterprise = models.CharField(max_length=255, blank=True, null=True)
    disbursement = models.CharField(max_length=255, blank=True, null=True)
    outstanding = models.CharField(max_length=255, blank=True, null=True)
    ln_recovery = models.CharField(max_length=255, blank=True, null=True)
    classified = models.CharField(max_length=255, blank=True, null=True)
    amount_others = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_me_q_sme_loan'


class ExtTPsDAsliBalances(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    ps_coa = models.CharField(max_length=255, blank=True, null=True)
    freq_ind_code = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    debit_credit_ind_code = models.CharField(max_length=255, blank=True, null=True)
    amount_usd = models.CharField(max_length=255, blank=True, null=True)
    banking_class = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_d_asli_balances'


class ExtTPsDLnProv(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    loan_class_id = models.CharField(max_length=255, blank=True, null=True)
    aging_range_id = models.CharField(max_length=255, blank=True, null=True)
    freq_ind_code = models.CharField(max_length=255, blank=True, null=True)
    amt_provision_reqd = models.CharField(max_length=255, blank=True, null=True)
    interest_suspense = models.CharField(max_length=255, blank=True, null=True)
    actual_provision = models.CharField(max_length=255, blank=True, null=True)
    base_for_provision = models.CharField(max_length=255, blank=True, null=True)
    outstanding_amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    insterest_suspense_against_sma = models.CharField(max_length=255, blank=True, null=True)
    value_of_eligible_securities = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_d_ln_prov'


class ExtTPsDLoanSpResSt(models.Model):
    dated = models.CharField(max_length=20, blank=True, null=True)
    fi_id = models.CharField(max_length=25, blank=True, null=True)
    facility_type = models.CharField(max_length=25, blank=True, null=True)
    application_no = models.CharField(max_length=25, blank=True, null=True)
    application_approved = models.CharField(max_length=25, blank=True, null=True)
    outstanding_amount = models.CharField(max_length=25, blank=True, null=True)
    down_payment_amount = models.CharField(max_length=25, blank=True, null=True)
    interest_suspense = models.CharField(max_length=25, blank=True, null=True)
    unapplied_interest = models.CharField(max_length=25, blank=True, null=True)
    interest_waived = models.CharField(max_length=25, blank=True, null=True)
    amount_rescheduled_exit = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_d_loan_sp_res_st'


class ExtTPsDSlrCashRes(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    ps_coa = models.CharField(max_length=255, blank=True, null=True)
    balance_bdt = models.CharField(max_length=255, blank=True, null=True)
    maintenance_date = models.CharField(max_length=255, blank=True, null=True)
    min_liquid_assets_reqd = models.CharField(max_length=255, blank=True, null=True)
    surplus_deficit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_d_slr_cash_res'


class ExtTPsMDpstSector(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    reporting_area_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_dpst_sector'


class ExtTPsMFiMonitorBr(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    ps_coa_id = models.CharField(max_length=255, blank=True, null=True)
    ps_coa_desc = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    islamic_conventional_ind = models.CharField(max_length=255, blank=True, null=True)
    office_ind = models.CharField(max_length=255, blank=True, null=True)
    amount_usd = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_fi_monitor_br'


class ExtTPsMFiMonitorHo(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    ps_coa_id = models.CharField(max_length=255, blank=True, null=True)
    ps_coa_desc = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    islamic_conventional_ind = models.CharField(max_length=255, blank=True, null=True)
    office_ind = models.CharField(max_length=255, blank=True, null=True)
    amount_usd = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_fi_monitor_ho'


class ExtTPsMIntRate(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    highest_interest_rate = models.CharField(max_length=255, blank=True, null=True)
    lowest_interest_rate = models.CharField(max_length=255, blank=True, null=True)
    freq_ind_code = models.CharField(max_length=255, blank=True, null=True)
    bank_classification = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_int_rate'


class ExtTPsMIntWaiver(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    waiver_amt_charge_debit_ac = models.CharField(max_length=255, blank=True, null=True)
    waiver_amt_charge_debit_int_su = models.CharField(max_length=255, blank=True, null=True)
    uncharged = models.CharField(max_length=255, blank=True, null=True)
    no_of_loan_accounts = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_int_waiver'


class ExtTPsMInterSa(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    aging_range_id = models.CharField(max_length=255, blank=True, null=True)
    account_type_code = models.CharField(max_length=255, blank=True, null=True)
    freq_ind_code = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    no_of_accounts = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_inter_sa'


class ExtTPsMInterTrx(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    orig_fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    resp_fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    unrecon_start = models.CharField(max_length=255, blank=True, null=True)
    unrecon_end = models.CharField(max_length=255, blank=True, null=True)
    debit_credit_ind_code = models.CharField(max_length=255, blank=True, null=True)
    aging_range_id = models.CharField(max_length=255, blank=True, null=True)
    freq_ind_code = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    transaction_count = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    advice_no = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_inter_trx'


class ExtTPsMLiqdtyFi(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    ps_coa_id = models.CharField(max_length=255, blank=True, null=True)
    aging_range = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_liqdty_fi'


class ExtTPsMReschedLoans(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    loan_lease_recipient = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    resched_step = models.CharField(max_length=255, blank=True, null=True)
    la_tl_no = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    sanction_date = models.CharField(max_length=255, blank=True, null=True)
    overdue_date = models.CharField(max_length=255, blank=True, null=True)
    reschedule_date = models.CharField(max_length=255, blank=True, null=True)
    sanction_amount = models.CharField(max_length=255, blank=True, null=True)
    overdue_amount = models.CharField(max_length=255, blank=True, null=True)
    down_payment = models.CharField(max_length=255, blank=True, null=True)
    percent_downpayment = models.CharField(max_length=255, blank=True, null=True)
    amount_rescheduled = models.CharField(max_length=255, blank=True, null=True)
    outstanding_amount_bdt = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_resched_loans'


class ExtTPsMSlrCrr(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    ps_coa = models.CharField(max_length=255, blank=True, null=True)
    maintain_month = models.CharField(max_length=255, blank=True, null=True)
    base_month = models.CharField(max_length=255, blank=True, null=True)
    w1_balance = models.CharField(max_length=255, blank=True, null=True)
    w2_balance = models.CharField(max_length=255, blank=True, null=True)
    w3_balance = models.CharField(max_length=255, blank=True, null=True)
    w4_balance = models.CharField(max_length=255, blank=True, null=True)
    w5_balance = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_slr_crr'


class ExtTPsMWriteOffLoanlease(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    lessee_loan = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    nature_of_loan_lease = models.CharField(max_length=255, blank=True, null=True)
    board_approval_no = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    legal_action_taken = models.CharField(max_length=255, blank=True, null=True)
    prosecution_no = models.CharField(max_length=255, blank=True, null=True)
    sanction_date = models.CharField(max_length=255, blank=True, null=True)
    bad_loan_date = models.CharField(max_length=255, blank=True, null=True)
    prosecution_date = models.CharField(max_length=255, blank=True, null=True)
    written_off_date = models.CharField(max_length=255, blank=True, null=True)
    approval_date = models.CharField(max_length=255, blank=True, null=True)
    provision_amount = models.CharField(max_length=255, blank=True, null=True)
    written_off_amount = models.CharField(max_length=255, blank=True, null=True)
    sanction_amount = models.CharField(max_length=255, blank=True, null=True)
    outstanding_amount = models.CharField(max_length=255, blank=True, null=True)
    bad_loan_amount = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_m_write_off_loanlease'


class ExtTPsQBankDirLoans(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    dir_fi_id = models.CharField(max_length=255, blank=True, null=True)
    collateral_id = models.CharField(max_length=4000, blank=True, null=True)
    borrower_name = models.CharField(max_length=255, blank=True, null=True)
    purpose = models.CharField(max_length=500, blank=True, null=True)
    bb_sanction_no = models.CharField(max_length=255, blank=True, null=True)
    loan_class_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    dos_id = models.CharField(max_length=255, blank=True, null=True)
    tax_identification_number = models.CharField(max_length=255, blank=True, null=True)
    nature_interest_code = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    approval_date_of_loan = models.CharField(max_length=255, blank=True, null=True)
    overdue_date_of_loan = models.CharField(max_length=255, blank=True, null=True)
    default_date_of_loan = models.CharField(max_length=255, blank=True, null=True)
    sanction_date = models.CharField(max_length=255, blank=True, null=True)
    validity_expiry_date = models.CharField(max_length=255, blank=True, null=True)
    bb_sanction_date = models.CharField(max_length=255, blank=True, null=True)
    overdue_amount = models.CharField(max_length=255, blank=True, null=True)
    total_outstanding_amt = models.CharField(max_length=255, blank=True, null=True)
    dir_funded_outs_amt = models.CharField(max_length=255, blank=True, null=True)
    indir_non_funded_outs_amt = models.CharField(max_length=255, blank=True, null=True)
    sanction_amount = models.CharField(max_length=255, blank=True, null=True)
    security_value = models.CharField(max_length=255, blank=True, null=True)
    default_amount = models.CharField(max_length=255, blank=True, null=True)
    perspective_code = models.CharField(max_length=255, blank=True, null=True)
    dir_borr_class = models.CharField(max_length=255, blank=True, null=True)
    remarks1 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_q_bank_dir_loans'


class ExtTPsQBaselBsl3(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    basel_coa = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    risk_weighted_assets = models.CharField(max_length=255, blank=True, null=True)
    amount_market_value = models.CharField(max_length=255, blank=True, null=True)
    cost_price = models.CharField(max_length=255, blank=True, null=True)
    capital_charge = models.CharField(max_length=255, blank=True, null=True)
    notional_amount = models.CharField(max_length=255, blank=True, null=True)
    cr_exposure = models.CharField(max_length=255, blank=True, null=True)
    ccf = models.CharField(max_length=255, blank=True, null=True)
    risk_weight = models.CharField(max_length=255, blank=True, null=True)
    market_price = models.CharField(max_length=255, blank=True, null=True)
    solo_consolidation_position = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_q_basel_bsl3'


class ExtTPsQFiDirLoans(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    dir_fi_id = models.CharField(max_length=255, blank=True, null=True)
    collateral_id = models.CharField(max_length=4000, blank=True, null=True)
    borrower_name = models.CharField(max_length=255, blank=True, null=True)
    purpose = models.CharField(max_length=4000, blank=True, null=True)
    bb_sanction_no = models.CharField(max_length=255, blank=True, null=True)
    loan_class_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    dos_id = models.CharField(max_length=255, blank=True, null=True)
    tax_identification_number = models.CharField(max_length=255, blank=True, null=True)
    nature_interest_code = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=4000, blank=True, null=True)
    approval_date_of_loan = models.CharField(max_length=255, blank=True, null=True)
    overdue_date_of_loan = models.CharField(max_length=255, blank=True, null=True)
    default_date_of_loan = models.CharField(max_length=255, blank=True, null=True)
    sanction_date = models.CharField(max_length=255, blank=True, null=True)
    validity_expiry_date = models.CharField(max_length=255, blank=True, null=True)
    bb_sanction_date = models.CharField(max_length=255, blank=True, null=True)
    overdue_amount = models.CharField(max_length=255, blank=True, null=True)
    total_outstanding_amt = models.CharField(max_length=255, blank=True, null=True)
    dir_funded_outs_amt = models.CharField(max_length=255, blank=True, null=True)
    indir_non_funded_outs_amt = models.CharField(max_length=255, blank=True, null=True)
    sanction_amount = models.CharField(max_length=255, blank=True, null=True)
    security_value = models.CharField(max_length=255, blank=True, null=True)
    default_amount = models.CharField(max_length=255, blank=True, null=True)
    perspective_code = models.CharField(max_length=255, blank=True, null=True)
    dir_borr_class = models.CharField(max_length=255, blank=True, null=True)
    remarks1 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_q_fi_dir_loans'


class ExtTPsQIntRate(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    highest_interest_rate = models.CharField(max_length=255, blank=True, null=True)
    lowest_interest_rate = models.CharField(max_length=255, blank=True, null=True)
    freq_ind_code = models.CharField(max_length=255, blank=True, null=True)
    bank_classification = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_q_int_rate'


class ExtTPsQLawsSuits(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    lawsuit_type_code = models.CharField(max_length=255, blank=True, null=True)
    case_type_code = models.CharField(max_length=255, blank=True, null=True)
    pending_period = models.CharField(max_length=255, blank=True, null=True)
    amount_claimed = models.CharField(max_length=255, blank=True, null=True)
    actual_recovery = models.CharField(max_length=255, blank=True, null=True)
    suit_count = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_q_laws_suits'


class ExtTPsQLnProv(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    fi_branch_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    loan_class_id = models.CharField(max_length=255, blank=True, null=True)
    aging_range_id = models.CharField(max_length=255, blank=True, null=True)
    freq_ind_code = models.CharField(max_length=255, blank=True, null=True)
    amt_provision_reqd = models.CharField(max_length=255, blank=True, null=True)
    interest_suspense = models.CharField(max_length=255, blank=True, null=True)
    actual_provision = models.CharField(max_length=255, blank=True, null=True)
    base_for_provision = models.CharField(max_length=255, blank=True, null=True)
    outstanding_amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    defaulted_outstanding = models.CharField(max_length=255, blank=True, null=True)
    insterest_suspense_against_sma = models.CharField(max_length=255, blank=True, null=True)
    value_of_eligible_securities = models.CharField(max_length=255, blank=True, null=True)
    report_type_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_q_ln_prov'


class ExtTPsQLnrecPosition(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    eco_sector_id = models.CharField(max_length=255, blank=True, null=True)
    amount_bdt = models.CharField(max_length=255, blank=True, null=True)
    curr_qtr_balance = models.CharField(max_length=255, blank=True, null=True)
    prev_qtr_cum_overdues = models.CharField(max_length=255, blank=True, null=True)
    curr_dues_recoverable = models.CharField(max_length=255, blank=True, null=True)
    loan_realised_cum_overdues = models.CharField(max_length=255, blank=True, null=True)
    loan_realised_rec_dues = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_q_lnrec_position'


class ExtTPsQLnrecRecovery(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    ps_coa = models.CharField(max_length=255, blank=True, null=True)
    product_type_id = models.CharField(max_length=255, blank=True, null=True)
    loan_class_id = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    loan_amt_bdt = models.CharField(max_length=255, blank=True, null=True)
    written_off_amount = models.CharField(max_length=255, blank=True, null=True)
    cash_recovery = models.CharField(max_length=255, blank=True, null=True)
    new_classified_advance = models.CharField(max_length=255, blank=True, null=True)
    resched_amount = models.CharField(max_length=255, blank=True, null=True)
    cumulative_written_off_amount = models.CharField(max_length=255, blank=True, null=True)
    prin_ln_waived_during_curr_qtr = models.CharField(max_length=255, blank=True, null=True)
    inst_ln_waived_during_curr_qtr = models.CharField(max_length=255, blank=True, null=True)
    prin_ln_writt_during_curr_qtr = models.CharField(max_length=255, blank=True, null=True)
    inst_ln_writt_during_curr_qtr = models.CharField(max_length=255, blank=True, null=True)
    r_agt_wrt_off_ln_dur_curr_qtr = models.CharField(max_length=255, blank=True, null=True)
    other_rcy_agt_classified_ln = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_q_lnrec_recovery'


class ExtTPsQShDirInfo(models.Model):
    dated = models.CharField(max_length=255, blank=True, null=True)
    fi_id = models.CharField(max_length=255, blank=True, null=True)
    director_name = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    dob = models.CharField(max_length=255, blank=True, null=True)
    nid = models.CharField(max_length=255, blank=True, null=True)
    tin = models.CharField(max_length=255, blank=True, null=True)
    passport_no = models.CharField(max_length=255, blank=True, null=True)
    fname = models.CharField(max_length=255, blank=True, null=True)
    mname = models.CharField(max_length=255, blank=True, null=True)
    sname = models.CharField(max_length=255, blank=True, null=True)
    present_address = models.CharField(max_length=255, blank=True, null=True)
    permanent_address = models.CharField(max_length=255, blank=True, null=True)
    educational_qualification = models.CharField(max_length=255, blank=True, null=True)
    work_experience = models.CharField(max_length=255, blank=True, null=True)
    date_of_first_appointment = models.CharField(max_length=255, blank=True, null=True)
    date_of_last_app_or_reapp = models.CharField(max_length=255, blank=True, null=True)
    interval_bet_subsequent_app = models.CharField(max_length=255, blank=True, null=True)
    fi_paid_up_capital = models.CharField(max_length=255, blank=True, null=True)
    no_of_shares_own = models.CharField(max_length=255, blank=True, null=True)
    total_no_of_shares = models.CharField(max_length=255, blank=True, null=True)
    total_face_value_shareholdings = models.CharField(max_length=255, blank=True, null=True)
    nominating_shareholder_name = models.CharField(max_length=255, blank=True, null=True)
    total_value_of_nm_holdings = models.CharField(max_length=255, blank=True, null=True)
    meeting_held = models.CharField(max_length=255, blank=True, null=True)
    meeting_attended = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    freq_indicator = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_t_ps_q_sh_dir_info'
