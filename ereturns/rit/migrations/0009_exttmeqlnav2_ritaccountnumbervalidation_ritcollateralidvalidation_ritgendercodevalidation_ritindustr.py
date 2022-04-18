# Generated by Django 3.2.12 on 2022-04-03 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rit', '0008_exttmeqsmeloan_ritloansegregationvalidation_ritsmecategoryvalidation_ritsmesubcategoryvalidation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtTMeQLnaV2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dated', models.CharField(blank=True, max_length=255, null=True)),
                ('fi_id', models.CharField(blank=True, max_length=255, null=True)),
                ('fi_branch_id', models.CharField(blank=True, max_length=255, null=True)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('account_holder_name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender_code', models.CharField(blank=True, max_length=255, null=True)),
                ('eco_sector_id', models.CharField(blank=True, max_length=255, null=True)),
                ('eco_purpose_id', models.CharField(blank=True, max_length=255, null=True)),
                ('industry_scale_id', models.CharField(blank=True, max_length=255, null=True)),
                ('collateral_id', models.CharField(blank=True, max_length=255, null=True)),
                ('product_type_id', models.CharField(blank=True, max_length=255, null=True)),
                ('loan_class_id', models.CharField(blank=True, max_length=255, null=True)),
                ('interest_rate', models.CharField(blank=True, max_length=255, null=True)),
                ('sanction_amount', models.CharField(blank=True, max_length=255, null=True)),
                ('opening_balance', models.CharField(blank=True, max_length=255, null=True)),
                ('disbursed_amount', models.CharField(blank=True, max_length=255, null=True)),
                ('recovered_amount', models.CharField(blank=True, max_length=255, null=True)),
                ('accrued_interest', models.CharField(blank=True, max_length=255, null=True)),
                ('other_charges', models.CharField(blank=True, max_length=255, null=True)),
                ('adjustment_amount', models.CharField(blank=True, max_length=255, null=True)),
                ('write_off_amount', models.CharField(blank=True, max_length=255, null=True)),
                ('outstanding_amount', models.CharField(blank=True, max_length=255, null=True)),
                ('overdue_amount', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'ext_t_me_q_lna_v2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RitLoanClassIdValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_class_id', models.IntegerField(blank=True, null=True, verbose_name='Loan Class Id')),
                ('rit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rit.ritfeatures')),
            ],
            options={
                'db_table': 'rit_validation_loan_class_id',
            },
        ),
        migrations.CreateModel(
            name='RitIndustryScaleIdValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_scale_id', models.IntegerField(blank=True, null=True, verbose_name='Industry Scale Id')),
                ('rit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rit.ritfeatures')),
            ],
            options={
                'db_table': 'rit_validation_industry_scale_id',
            },
        ),
        migrations.CreateModel(
            name='RitGenderCodeValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender_code', models.IntegerField(blank=True, null=True, verbose_name='Gender Code')),
                ('rit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rit.ritfeatures')),
            ],
            options={
                'db_table': 'rit_validation_gender_code',
            },
        ),
        migrations.CreateModel(
            name='RitCollateralIdValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collateral_id', models.IntegerField(blank=True, null=True, verbose_name='Collateral Id')),
                ('rit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rit.ritfeatures')),
            ],
            options={
                'db_table': 'rit_validation_collateral_id',
            },
        ),
        migrations.CreateModel(
            name='RitAccountNumberValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.IntegerField(blank=True, null=True, verbose_name='Account Number')),
                ('rit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rit.ritfeatures')),
            ],
            options={
                'db_table': 'rit_validation_account_number',
            },
        ),
    ]