from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, Lawyer
from contact.models import Request
from invoice.models import Invoice
from chat.models import Case, Message


class Command(BaseCommand):
    help = 'Seed demo data: lawyer, sample requests, invoices, a paid case with chat'

    def handle(self, *args, **options):
        # Lawyer
        if not User.objects.filter(username='lawyer1').exists():
            lu = User.objects.create_user(
                username='lawyer1', password='lawyer123',
                first_name='Alisher', last_name='Karimov',
                role=User.ROLE_LAWYER,
            )
            lawyer = Lawyer.objects.create(user=lu, direction='family', phone='+998901234567')
            self.stdout.write(self.style.SUCCESS('Created lawyer: lawyer1 / lawyer123'))
        else:
            lawyer = Lawyer.objects.get(user__username='lawyer1')

        # Request 1: new
        r1, _ = Request.objects.get_or_create(
            customer_name='Demo Client (New)',
            defaults=dict(
                phone='+998901111111',
                text='I need help with a family dispute regarding property division.',
                source='site',
                status='new',
            ),
        )

        # Request 2: offered (invoice ready, awaiting payment)
        r2, created = Request.objects.get_or_create(
            customer_name='Demo Client (Offered)',
            defaults=dict(
                phone='+998902222222',
                text='My employer has not paid my salary for 3 months.',
                source='site',
                status='offered',
                direction='labor',
                total_amount=1_000_000,
            ),
        )
        if created or not hasattr(r2, 'invoice'):
            Invoice.objects.get_or_create(
                request=r2,
                defaults=dict(
                    invoice_number=Invoice.generate_number(),
                    ten_percent_amount=100_000,
                ),
            )

        # Request 3: paid + assigned + chat messages
        r3, created = Request.objects.get_or_create(
            customer_name='Demo Client (Paid)',
            defaults=dict(
                phone='+998903333333',
                text='I need a contract reviewed before signing.',
                source='bot',
                status='assigned',
                direction='contract',
                total_amount=500_000,
            ),
        )
        if created or not hasattr(r3, 'invoice'):
            Invoice.objects.create(
                request=r3,
                invoice_number=Invoice.generate_number(),
                ten_percent_amount=50_000,
                paid=True,
                paid_date=timezone.now(),
                paid_amount=50_000,
                payment_method='payme',
            )

        case, _ = Case.objects.get_or_create(
            request=r3,
            defaults={'lawyer': lawyer, 'status': 'in_progress'},
        )

        if not case.messages.exists():
            Message.objects.create(case=case, sender='client', sender_name='Demo Client (Paid)', text='Hello, I uploaded the contract. Please review clause 5.')
            Message.objects.create(case=case, sender='lawyer', sender_name='Alisher Karimov', text='Hello! I reviewed clause 5. It has an unfavorable penalty clause. I recommend negotiating it down.')
            Message.objects.create(case=case, sender='client', sender_name='Demo Client (Paid)', text='Thank you! What should I say to the other party?')

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully!'))
        self.stdout.write('')
        self.stdout.write(f'  Request #{r1.pk}  - New          ->  /status/?id={r1.pk}')
        self.stdout.write(f'  Request #{r2.pk}  - Offered      ->  /payment/{r2.pk}/')
        self.stdout.write(f'  Request #{r3.pk}  - Paid+Assigned ->  /cabinet/{r3.pk}/')
        self.stdout.write('')
        self.stdout.write('Logins:')
        self.stdout.write('  Admin:  admin / admin123   ->  /admin-panel/')
        self.stdout.write('  Lawyer: lawyer1 / lawyer123 ->  /lawyer/')
