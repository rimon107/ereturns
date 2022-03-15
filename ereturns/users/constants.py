class Status:
    OFFLINE = 0
    ONLINE = 1

    Status = (
        (ONLINE, 'Online'),
        (OFFLINE, 'Offline'),
    )


class GroupNames:
    bb_admin = "BB Admin"
    bb_end_user = "BB End User"
    bank_branch_end_user = "Bank Branch End User"
    bank_ho_end_user = "Bank HO End User"
    bank_ho_admin = "Bank HO Admin"
