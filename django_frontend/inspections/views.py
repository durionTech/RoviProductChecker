from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from django.shortcuts import render
from .models import Inspection

def inspect_product(request):

    if request.method == "POST":

        front_image = request.FILES.get("front_image")
        back_image = request.FILES.get("back_image")
        side_image = request.FILES.get("side_image")

        # Front image is required
        if not front_image:
            return render(
                request,
                "dashboard.html",
                {
                    "error": "Please upload a front image."
                }
            )

        files = {
            "front_image": (
                front_image.name,
                front_image,
                front_image.content_type
            )
        }

        # Add optional back image
        if back_image:
            files["back_image"] = (
                back_image.name,
                back_image,
                back_image.content_type
            )

        # Add optional side image
        if side_image:
            files["side_image"] = (
                side_image.name,
                side_image,
                side_image.content_type
            )

        try:

            response = requests.post(
                settings.FASTAPI_INSPECTION_URL,
                files=files,
                timeout=120
            )

            response.raise_for_status()

            inspection_result = response.json()

            return render(
                request,
                "dashboard.html",
                {
                    "result": inspection_result
                }
            )

        except requests.exceptions.ConnectionError:

            return render(
                request,
                "dashboard.html",
                {
                    "error": "Cannot connect to FastAPI server. Please start FastAPI on port 8001."
                }
            )

        except requests.exceptions.Timeout:

            return render(
                request,
                "dashboard.html",
                {
                    "error": "Inspection took too long. Please try again."
                }
            )

        except requests.exceptions.RequestException as e:

            return render(
                request,
                "dashboard.html",
                {
                    "error": f"API Error: {str(e)}"
                }
            )

    return render(request, "dashboard.html")

@login_required
def dashboard(request):

    inspections = Inspection.objects.all().order_by('-created_at')

    total = inspections.count()

    passed = inspections.filter(status='PASS').count()

    failed = inspections.filter(status='FAIL').count()

    pending = inspections.filter(
        status__in=['PENDING', 'PROCESSING']
    ).count()

    context = {
        'inspections': inspections[:10],
        'total': total,
        'passed': passed,
        'failed': failed,
        'pending': pending,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


# @login_required
# def upload_product(request):

#     if request.method == 'POST':

#         inspection = Inspection.objects.create(

#             inspector=request.user,

#             product_name=request.POST.get(
#                 'product_name',
#                 ''
#             ),

#             front_image=request.FILES.get(
#                 'front_image'
#             ),

#             back_image=request.FILES.get(
#                 'back_image'
#             ),

#             side_image=request.FILES.get(
#                 'side_image'
#             ),

#             status='PENDING'
#         )

#         return redirect(
#             'inspection_detail',
#             inspection_id=inspection.id
#         )

#     return render(
#         request,
#         'upload.html'
#     )

@login_required
def upload_product(request):

    if request.method == 'POST':

        front_image = request.FILES.get('front_image')
        back_image = request.FILES.get('back_image')
        side_image = request.FILES.get('side_image')

        # Front image is mandatory
        if not front_image:
            return render(
                request,
                'upload.html',
                {
                    'error': 'Please upload a front image.'
                }
            )

        # ==========================================
        # 1. CREATE DJANGO INSPECTION
        # ==========================================

        inspection = Inspection.objects.create(

            inspector=request.user,

            product_name=request.POST.get(
                'product_name',
                ''
            ),

            front_image=front_image,

            back_image=back_image,

            side_image=side_image,

            status='PROCESSING'
        )


        try:

            # ==========================================
            # 2. OPEN SAVED IMAGES
            # ==========================================

            files = {}
            opened_files = []


            # FRONT IMAGE
            if inspection.front_image:

                front_file = inspection.front_image.open('rb')

                files['front_image'] = (
                    inspection.front_image.name,
                    front_file,
                    'image/jpeg'
                )

                opened_files.append(front_file)


            # BACK IMAGE
            if inspection.back_image:

                back_file = inspection.back_image.open('rb')

                files['back_image'] = (
                    inspection.back_image.name,
                    back_file,
                    'image/jpeg'
                )

                opened_files.append(back_file)


            # SIDE IMAGE
            if inspection.side_image:

                side_file = inspection.side_image.open('rb')

                files['side_image'] = (
                    inspection.side_image.name,
                    side_file,
                    'image/jpeg'
                )

                opened_files.append(side_file)


            # ==========================================
            # 3. SEND TO FASTAPI
            # ==========================================

            print('\n========================================')
            print('SENDING IMAGES TO FASTAPI...')
            print('========================================')


            response = requests.post(

                settings.FASTAPI_INSPECTION_URL,

                files=files,

                timeout=120
            )


            response.raise_for_status()


            # ==========================================
            # 4. GET FASTAPI RESULT
            # ==========================================

            result = response.json()


            print('\n========================================')
            print('FASTAPI RESPONSE:')
            print(result)
            print('========================================')


            # Save complete API response
            inspection.ocr_result = result


            # ==========================================
            # 5. SAVE COMBINED OCR TEXT
            # ==========================================

            inspection.extracted_text = result.get(
                'combined_text',
                ''
            )


            # ==========================================
            # 6. GET EXTRACTED FIELDS
            # ==========================================

            extracted_fields = result.get(
                'extracted_fields',
                {}
            )


            # MRP
            mrp_data = extracted_fields.get(
                'mrp',
                {}
            )

            if isinstance(mrp_data, dict):
                inspection.extracted_mrp = mrp_data.get(
                    'value',
                    ''
                )
            else:
                inspection.extracted_mrp = str(
                    mrp_data or ''
                )


            # NET QUANTITY
            quantity_data = extracted_fields.get(
                'net_quantity',
                {}
            )

            if isinstance(quantity_data, dict):
                inspection.extracted_net_quantity = quantity_data.get(
                    'value',
                    ''
                )
            else:
                inspection.extracted_net_quantity = str(
                    quantity_data or ''
                )


            # MANUFACTURER
            manufacturer_data = extracted_fields.get(
                'manufacturer',
                {}
            )

            if isinstance(manufacturer_data, dict):
                inspection.extracted_manufacturer = manufacturer_data.get(
                    'value',
                    ''
                )
            else:
                inspection.extracted_manufacturer = str(
                    manufacturer_data or ''
                )


            # DATE
            date_data = extracted_fields.get(
                'manufacture_date',
                {}
            )

            if isinstance(date_data, dict):
                inspection.extracted_date = date_data.get(
                    'value',
                    ''
                )
            else:
                inspection.extracted_date = str(
                    date_data or ''
                )


            # ==========================================
            # 7. SAVE COMPLIANCE RESULT
            # ==========================================

            compliance_result = result.get(
                'compliance_result',
                {}
            )


            status = compliance_result.get(
                'status',
                ''
            ).upper()


            if status in ['PASS', 'FAIL']:

                inspection.status = status

            else:

                # Temporary status based on OCR
                # until rule engine is added
                inspection.status = 'PASS'


            # ==========================================
            # 8. SAVE VIOLATIONS
            # ==========================================

            inspection.violations = compliance_result.get(
                'violations',
                []
            )


            # ==========================================
            # 9. SAVE DATABASE
            # ==========================================

            inspection.save()


            print('\nINSPECTION SAVED SUCCESSFULLY')
            print('Inspection ID:', inspection.id)
            print('Status:', inspection.status)
            print('MRP:', inspection.extracted_mrp)
            print('Quantity:', inspection.extracted_net_quantity)
            print('Manufacturer:', inspection.extracted_manufacturer)
            print('Date:', inspection.extracted_date)


        except requests.exceptions.ConnectionError:

            inspection.status = 'ERROR'

            inspection.violations = [
                {
                    'rule': 'SYSTEM',
                    'message': 'Cannot connect to FastAPI server.'
                }
            ]

            inspection.save()


        except requests.exceptions.Timeout:

            inspection.status = 'ERROR'

            inspection.violations = [
                {
                    'rule': 'SYSTEM',
                    'message': 'FastAPI inspection timed out.'
                }
            ]

            inspection.save()


        except Exception as e:

            print('\nDJANGO PROCESSING ERROR:')
            print(str(e))


            inspection.status = 'ERROR'

            inspection.violations = [
                {
                    'rule': 'SYSTEM',
                    'message': str(e)
                }
            ]

            inspection.save()


        finally:

            # ==========================================
            # CLOSE FILES
            # ==========================================

            if 'opened_files' in locals():

                for file_obj in opened_files:

                    try:
                        file_obj.close()
                    except Exception:
                        pass


        # ==========================================
        # 10. REDIRECT TO RESULT PAGE
        # ==========================================

        return redirect(
            'inspection_detail',
            inspection_id=inspection.id
        )


    return render(
        request,
        'upload.html'
    )

@login_required
def inspection_detail(request, inspection_id):

    inspection = get_object_or_404(
        Inspection,
        id=inspection_id
    )

    return render(
        request,
        'inspection_detail.html',
        {
            'inspection': inspection
        }
    )