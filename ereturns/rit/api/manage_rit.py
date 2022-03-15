from ereturns.rit.tasks import (
    insert_rit_t_me_d_frx_ech_pos,
    insert_rit_t_ps_d_loan_sp_res_st, insert_rit_t_me_m_ass_liab_supp_sbs, insert_rit_t_me_m_ass_liab_fin,
    insert_rit_t_me_m_ass_liab_obu, insert_rit_t_me_m_ass_liab_bank
)


class ManageRit:

    def __init__(self):
        self.db = 'rit_mngt'

    def insert_into_db(self, uploaded_rit):
        name = uploaded_rit.rit.name
        id = uploaded_rit.id
        if name.lower() == "t_me_d_frx_ech_pos":
            insert_rit_t_me_d_frx_ech_pos.delay(id, self.db)
        if name.lower() == "t_ps_d_loan_sp_res_st":
            insert_rit_t_ps_d_loan_sp_res_st.delay(id, self.db)
        if name.lower() == "t_me_m_ass_liab_supplementary_sbs1":
            insert_rit_t_me_m_ass_liab_supp_sbs.delay(id, self.db)
        if name.lower() == "t_me_m_ass_liab_fin":
            insert_rit_t_me_m_ass_liab_fin.delay(id, self.db)
        if name.lower() == "t_me_m_ass_liab_obu":
            insert_rit_t_me_m_ass_liab_obu.delay(id, self.db)
        if name.lower() == "t_me_m_ass_liab_bank":
            insert_rit_t_me_m_ass_liab_bank.delay(id, self.db)
