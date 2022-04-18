from ereturns.rit.tasks import (
    insert_rit_t_me_d_frx_ech_pos,
    insert_rit_t_ps_d_loan_sp_res_st,
    insert_rit_t_me_m_ass_liab_supp_sbs,
    insert_rit_t_me_m_ass_for,
    insert_rit_t_me_m_ass_for_obu,
    insert_rit_t_me_m_ass_liab,
    insert_rit_t_me_m_ass_liab_obu, insert_rit_t_me_m_lna_dl, insert_rit_t_me_m_lna_dl_obu,
    insert_rit_t_me_m_ebanking_ecommerce, insert_rit_t_me_m_port_inv, insert_rit_t_me_m_port_survey,
    insert_rit_t_me_q_inv_non_res_fi, insert_rit_t_me_m_frc_trn, insert_rit_t_me_m_frc_trn_supp,
    insert_rit_t_me_m_lna_rates, insert_rit_t_me_m_depo_dri, insert_rit_t_me_d_remittance,
    insert_rit_t_me_q_inv_for_fi_1, insert_rit_t_me_q_inv_for_fi_2, insert_rit_t_me_q_acep, insert_rit_t_me_m_sted,
    insert_rit_t_me_q_sme_loan, insert_rit_t_me_q_lna_v2, insert_rit_t_ps_d_asli_balances, insert_rit_t_ps_m_inter_sa,
    insert_rit_t_ps_m_inter_trx, insert_rit_t_ps_m_dpst_sector, insert_rit_t_ps_m_int_waiver,
    insert_rit_t_ps_m_int_rate, insert_rit_t_ps_d_ln_prov, insert_rit_t_ps_d_slr_cash_res, insert_rit_t_ps_q_laws_suits,
    insert_rit_t_ps_q_ln_prov, insert_rit_t_ps_q_int_rate, insert_rit_t_ps_q_lnrec_position,
    insert_rit_t_ps_q_lnrec_recovery, insert_rit_t_ps_q_sh_dir_info, insert_rit_t_ps_q_bank_dir_loans,
    insert_rit_t_ps_q_fi_dir_loans, insert_rit_t_ps_m_nbfi_monitor_br, insert_rit_t_ps_m_nbfi_monitor_ho,
    insert_rit_t_ps_q_basel_bsl3, insert_rit_t_me_q_depo_cls_v2, insert_rit_t_ps_m_liqdty_fi,
    insert_rit_t_ps_m_resched_loans, insert_rit_t_ps_m_slr_crr, insert_rit_t_ps_m_write_off_loanlease,
    insert_rit_t_me_m_inr_non_res, insert_rit_t_me_q_lted_transaction, insert_rit_t_ps_m_fi_monitor_ho,
    insert_rit_t_ps_m_fi_monitor_br
)


class ManageRit:

    def __init__(self):
        self.db = 'rit_mngt'

    def insert_into_db(self, uploaded_rit, meta):
        name = uploaded_rit.rit.name
        uploaded_rit_id = uploaded_rit.id
        if name.lower() == "t_me_d_frx_ech_pos":
            insert_rit_t_me_d_frx_ech_pos.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_d_loan_sp_res_st":
            insert_rit_t_ps_d_loan_sp_res_st.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_ass_liab_supplementary_sbs1":
            insert_rit_t_me_m_ass_liab_supp_sbs.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_ass_for":
            insert_rit_t_me_m_ass_for.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_ass_for_obu":
            insert_rit_t_me_m_ass_for_obu.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_ass_liab":
            insert_rit_t_me_m_ass_liab.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_ass_liab_obu":
            insert_rit_t_me_m_ass_liab_obu.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_lna_dl":
            insert_rit_t_me_m_lna_dl.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_lna_dl_obu":
            insert_rit_t_me_m_lna_dl_obu.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_ebanking_ecommerce":
            insert_rit_t_me_m_ebanking_ecommerce.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_port_inv":
            insert_rit_t_me_m_port_inv.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_port_survey":
            insert_rit_t_me_m_port_survey.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_q_inv_non_res_fi_1":
            insert_rit_t_me_q_inv_non_res_fi.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_q_inv_non_res_fi_2":
            insert_rit_t_me_q_inv_non_res_fi.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_frc_trn":
            insert_rit_t_me_m_frc_trn.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_frc_trn_supp":
            insert_rit_t_me_m_frc_trn_supp.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_lna_rates":
            insert_rit_t_me_m_lna_rates.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_depo_dri":
            insert_rit_t_me_m_depo_dri.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_d_remittance":
            insert_rit_t_me_d_remittance.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_q_inv_for_fi_1":
            insert_rit_t_me_q_inv_for_fi_1.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_q_inv_for_fi_2":
            insert_rit_t_me_q_inv_for_fi_2.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_q_acep":
            insert_rit_t_me_q_acep.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_sted":
            insert_rit_t_me_m_sted.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_q_sme_loan":
            insert_rit_t_me_q_sme_loan.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_q_lna_v2":
            insert_rit_t_me_q_lna_v2.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_d_asli_balances":
            insert_rit_t_ps_d_asli_balances.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_inter_sa":
            insert_rit_t_ps_m_inter_sa.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_inter_trx":
            insert_rit_t_ps_m_inter_trx.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_dpst_sector":
            insert_rit_t_ps_m_dpst_sector.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_int_waiver":
            insert_rit_t_ps_m_int_waiver.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_int_waiver":
            insert_rit_t_ps_m_int_waiver.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_int_rate":
            insert_rit_t_ps_m_int_rate.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_d_ln_prov":
            insert_rit_t_ps_d_ln_prov.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_d_slr_cash_res":
            insert_rit_t_ps_d_slr_cash_res.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_q_laws_suits":
            insert_rit_t_ps_q_laws_suits.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_q_ln_prov":
            insert_rit_t_ps_q_ln_prov.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_q_int_rate":
            insert_rit_t_ps_q_int_rate.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_q_lnrec_position":
            insert_rit_t_ps_q_lnrec_position.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_q_lnrec_recovery":
            insert_rit_t_ps_q_lnrec_recovery.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_q_sh_dir_info":
            insert_rit_t_ps_q_sh_dir_info.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_q_bank_dir_loans":
            insert_rit_t_ps_q_bank_dir_loans.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_q_fi_dir_loans":
            insert_rit_t_ps_q_fi_dir_loans.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_nbfi_monitor_br":
            insert_rit_t_ps_m_nbfi_monitor_br.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_nbfi_monitor_ho":
            insert_rit_t_ps_m_nbfi_monitor_ho.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_q_basel_bsl3":
            insert_rit_t_ps_q_basel_bsl3.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_q_depo_cls_v2":
            insert_rit_t_me_q_depo_cls_v2.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_liqdty_fi":
            insert_rit_t_ps_m_liqdty_fi.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_resched_loans":
            insert_rit_t_ps_m_resched_loans.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_slr_crr":
            insert_rit_t_ps_m_slr_crr.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_write_off_loanlease":
            insert_rit_t_ps_m_write_off_loanlease.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_m_inr_non_res":
            insert_rit_t_me_m_inr_non_res.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_me_q_lted_transaction":
            insert_rit_t_me_q_lted_transaction.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_fi_monitor_br":
            insert_rit_t_ps_m_fi_monitor_br.delay(uploaded_rit_id, self.db, meta)
        if name.lower() == "t_ps_m_fi_monitor_ho":
            insert_rit_t_ps_m_fi_monitor_ho.delay(uploaded_rit_id, self.db, meta)
