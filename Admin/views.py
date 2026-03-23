from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from users.models import UserRegistrationModel, PredictionHistory
import pandas as pd
import os


def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('password')
        print("User ID is = ", usrid)

        # Admin credentials
        if (usrid == 'Admin' and pswd == 'Admin@123') or \
           (usrid == 'Sathvika' and pswd == 'Sathvika@123'):
            request.session['admin_user'] = usrid
            request.session['loggeduser'] = usrid
            request.session['loginid'] = usrid
            return render(request, 'admins/AdminHome.html', {'admin_name': usrid})
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def RegisterUsersView(request):
    data = UserRegistrationModel.objects.all()
    # Get unread notification count (safely handle if table doesn't exist yet)
    unread_count = 0
    return render(request, 'admins/viewregisterusers.html', context={'data': data, 'unread_count': unread_count})


def ActivaUsers(request):
    if request.method == 'GET':
        user_id = request.GET.get('uid')

        if user_id:
            status = 'activated'
            print("Activating user with ID =", user_id)
            UserRegistrationModel.objects.filter(id=user_id).update(status=status)

        return redirect('RegisterUsersView')


def DeleteUsers(request):
    """Delete user and all related data"""
    if request.method == 'GET':
        user_id = request.GET.get('uid')

        if user_id:
            print("Deleting user with ID =", user_id)
            try:
                # Get user before deleting (for logging)
                user = UserRegistrationModel.objects.get(id=user_id)
                user_name = user.name
                user_loginid = user.loginid
                
                # Delete all prediction history for this user
                PredictionHistory.objects.filter(user=user).delete()
                print(f"Deleted prediction history for user {user_name}")
                
                # Delete the user (CASCADE will handle other related data if any)
                UserRegistrationModel.objects.filter(id=user_id).delete()
                print(f"Successfully deleted user: {user_name} ({user_loginid})")
                
                messages.success(request, f'User "{user_name}" and all related data deleted successfully!')
            except UserRegistrationModel.DoesNotExist:
                messages.error(request, 'User not found!')
            except Exception as e:
                print(f"Error deleting user: {str(e)}")
                messages.error(request, f'Error deleting user: {str(e)}')

        # Redirect to admin home first to ensure admin session is maintained
        return redirect('AdminHome')


def viewUserDetails(request):
    """View detailed user information with prediction history"""
    if request.method == 'GET':
        user_id = request.GET.get('uid')

        if user_id:
            try:
                user = UserRegistrationModel.objects.get(id=user_id)
                # Get prediction history for this user
                predictions = PredictionHistory.objects.filter(user=user).order_by('-timestamp')
                
                # Calculate prediction stats
                total_predictions = predictions.count()
                
                # Group by cell type for statistics
                cell_counts = {}
                confidence_sum = 0
                for pred in predictions:
                    cell_name = pred.cell_name
                    cell_counts[cell_name] = cell_counts.get(cell_name, 0) + 1
                    confidence_sum += pred.confidence
                
                avg_confidence = round(confidence_sum / total_predictions, 2) if total_predictions > 0 else 0
                cell_labels = list(cell_counts.keys())
                cell_values = list(cell_counts.values())
                
                return render(request, 'admins/user_details.html', {
                    'user': user,
                    'predictions': predictions,
                    'total_predictions': total_predictions,
                    'avg_confidence': avg_confidence,
                    'cell_labels': cell_labels,
                    'cell_values': cell_values
                })
            except UserRegistrationModel.DoesNotExist:
                messages.error(request, 'User not found!')
                return redirect('RegisterUsersView')

    return redirect('RegisterUsersView')


def adminNotifications(request):
    """View all admin notifications"""
    notifications = []
    unread_count = 0
    try:
        from Admin.models import NotificationModel
        notifications = NotificationModel.objects.all().order_by('-created_at')
        unread_count = notifications.filter(is_read=False).count()
    except:
        pass
    
    return render(request, 'admins/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


def markAdminNotificationRead(request):
    """Mark admin notification as read"""
    if request.method == 'GET':
        notif_id = request.GET.get('id')
        if notif_id:
            try:
                from Admin.models import NotificationModel
                NotificationModel.objects.filter(id=notif_id).update(is_read=True)
            except:
                pass
    return redirect('adminNotifications')


def passwordResetRequests(request):
    """View and manage password reset requests"""
    requests = []
    pending_requests = []
    try:
        from Admin.models import PasswordResetRequestModel
        requests = PasswordResetRequestModel.objects.all().order_by('-created_at')
        pending_requests = requests.filter(status='pending')
    except:
        pass

    return render(request, 'admins/password_reset_requests.html', {
        'requests': requests,
        'pending_requests': pending_requests
    })


def approvePasswordReset(request):
    """Approve password reset request"""
    if request.method == 'GET':
        request_id = request.GET.get('id')

        if request_id:
            try:
                from Admin.models import PasswordResetRequestModel
                reset_request = PasswordResetRequestModel.objects.get(id=request_id)
                reset_request.status = 'approved'
                reset_request.resolved_at = timezone.now()

                # Update user's password
                if reset_request.new_password:
                    reset_request.user.password = reset_request.new_password
                    reset_request.user.save()

                reset_request.save()
                messages.success(request, 'Password reset approved!')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')

    return redirect('passwordResetRequests')


def rejectPasswordReset(request):
    """Reject password reset request"""
    if request.method == 'GET':
        request_id = request.GET.get('id')

        if request_id:
            try:
                from Admin.models import PasswordResetRequestModel
                reset_request = PasswordResetRequestModel.objects.get(id=request_id)
                reset_request.status = 'rejected'
                reset_request.resolved_at = timezone.now()
                reset_request.save()
                messages.success(request, 'Password reset rejected!')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')

    return redirect('passwordResetRequests')


def helpTickets(request):
    """View all help tickets"""
    tickets = []
    pending_tickets = []
    try:
        from Admin.models import HelpTicketModel
        tickets = HelpTicketModel.objects.all().order_by('-created_at')
        pending_tickets = tickets.filter(status='pending')
    except:
        pass

    return render(request, 'admins/help_tickets.html', {
        'tickets': tickets,
        'pending_tickets': pending_tickets
    })


def markHelpTicketSolved(request):
    """Mark help ticket as solved"""
    if request.method == 'GET':
        ticket_id = request.GET.get('id')
        response = request.GET.get('response', '')

        if ticket_id:
            try:
                from Admin.models import HelpTicketModel
                ticket = HelpTicketModel.objects.get(id=ticket_id)
                ticket.status = 'solved'
                ticket.admin_response = response
                ticket.resolved_at = timezone.now()
                ticket.save()
                messages.success(request, 'Ticket marked as solved!')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')

    return redirect('helpTickets')


def markHelpTicketInProgress(request):
    """Mark help ticket as in progress"""
    if request.method == 'GET':
        ticket_id = request.GET.get('id')

        if ticket_id:
            try:
                from Admin.models import HelpTicketModel
                HelpTicketModel.objects.filter(id=ticket_id).update(status='in_progress')
                messages.success(request, 'Ticket status updated!')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')

    return redirect('helpTickets')


