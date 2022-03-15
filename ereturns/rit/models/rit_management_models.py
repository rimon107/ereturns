from django.db import models


class DDates(models.Model):
    use_db = 'rit_mngt'
    date_id = models.BigIntegerField(primary_key=True)
    cal_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_dates'


class StgTMeDFrxEchPos(models.Model):
    use_db = 'rit_mngt'
    date_id = models.FloatField(primary_key=True, unique=False)
    ccy_id = models.FloatField()
    fi_id = models.FloatField()
    monetary_coa_id = models.FloatField()
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    amount_fcy = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    user_code = models.IntegerField(blank=True, null=True)
    load_date = models.DateField(blank=True, null=True)
    identity_code = models.IntegerField(blank=True, null=True)
    valid_ind = models.BooleanField()
    ref_err = models.CharField(max_length=200, blank=True, null=True)
    open_position_limit = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_t_me_d_frx_ech_pos'


class StgTPsDLoanSpResSt(models.Model):
    date_id = models.FloatField()
    fi_id = models.FloatField()
    facility_type = models.IntegerField(blank=True, null=True)
    application_no = models.IntegerField(blank=True, null=True)
    application_approved = models.IntegerField(blank=True, null=True)
    outstanding_amount = models.DecimalField(max_digits=22, decimal_places=6, blank=True, null=True)
    down_payment_amount = models.DecimalField(max_digits=22, decimal_places=6, blank=True, null=True)
    interest_suspense = models.DecimalField(max_digits=22, decimal_places=6, blank=True, null=True)
    unapplied_interest = models.DecimalField(max_digits=22, decimal_places=6, blank=True, null=True)
    interest_waived = models.DecimalField(max_digits=22, decimal_places=6, blank=True, null=True)
    amount_rescheduled_exit = models.DecimalField(max_digits=22, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_t_ps_d_loan_sp_res_st'


class StgTMeMAssLiabBank(models.Model):
    date_id = models.FloatField(blank=True, null=True)
    fi_id = models.FloatField(blank=True, null=True)
    monetary_coa_id = models.FloatField(blank=True, null=True)
    amount_bdt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    user_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_t_me_m_ass_liab_bank'


class StgTMeMAssLiabFin(models.Model):
    date_id = models.FloatField(blank=True, null=True)
    fi_id = models.FloatField(blank=True, null=True)
    monetary_coa_id = models.FloatField(blank=True, null=True)
    amount_bdt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    user_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_t_me_m_ass_liab_fin'


class StgTMeMAssLiabObu(models.Model):
    date_id = models.FloatField(blank=True, null=True)
    fi_id = models.FloatField(blank=True, null=True)
    monetary_coa_id = models.FloatField(blank=True, null=True)
    amount_bdt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    user_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_t_me_m_ass_liab_obu'


class StgTMeMAssLiabSuppSbs(models.Model):
    date_id = models.FloatField(blank=True, null=True)
    fi_id = models.FloatField(blank=True, null=True)
    monetary_coa_id = models.FloatField(blank=True, null=True)
    amount_bdt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    user_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stg_t_me_m_ass_liab_supp_sbs'
