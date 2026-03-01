"""
API routes for Report_History table (APIs 11 & 12)
SELECT operations (API 11) and CRUD operations (API 12)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from app.database import get_db
from app.services.report_service import ReportService
from app.schemas.report import ReportCreate, ReportUpdate
from app.schemas.common import APIResponse
from app.constants import HTTPStatus

router = APIRouter(prefix="/reports", tags=["Reports"])


# API 11: SELECT - Get all reports
@router.get("/all", response_model=APIResponse)
async def get_all_reports(
    db=Depends(get_db),
    status: str = Query(None),
    report_type: str = Query(None),
    user_id: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    API 11: SELECT Operation - Retrieve all medical reports
    - Returns all reports with optional filtering
    - Supports pagination with limit and offset
    """
    try:
        reports = await ReportService.get_all_reports(
            db, status, report_type, user_id, limit, offset
        )

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="Reports retrieved successfully",
            data={"reports": reports, "count": len(reports)},
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# API 12: CRUD - Create report
@router.post("", response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create_report(
    report_data: ReportCreate,
    db=Depends(get_db)
):
    """
    API 12: CRUD Operation - Create new medical report
    - Creates a new report with provided data
    - Returns the created report
    """
    try:
        # Check if report already exists
        existing = await ReportService.get_report_by_id(db, report_data.id)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Report {report_data.id} already exists"
            )

        new_report = await ReportService.create_report(db, report_data.dict())

        return APIResponse(
            status="success",
            code=HTTPStatus.CREATED,
            message="Report created successfully",
            data={"report": new_report},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 12: CRUD - Update report
@router.put("/{reportId}", response_model=APIResponse)
async def update_report(
    reportId: str,
    report_data: ReportUpdate,
    db=Depends(get_db)
):
    """
    API 12: CRUD Operation - Update medical report
    - Updates an existing report
    - Returns the updated report
    """
    try:
        # Check if report exists
        existing = await ReportService.get_report_by_id(db, reportId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Report {reportId} not found"
            )

        updated_report = await ReportService.update_report(
            db, reportId, report_data.dict(exclude_unset=True)
        )

        return APIResponse(
            status="success",
            code=HTTPStatus.OK,
            message="Report updated successfully",
            data={"report": updated_report},
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


# API 12: CRUD - Delete report
@router.delete("/{reportId}", status_code=HTTPStatus.NO_CONTENT)
async def delete_report(
    reportId: str,
    db=Depends(get_db)
):
    """
    API 12: CRUD Operation - Delete medical report
    - Deletes a report by ID
    - Returns 204 No Content on success
    """
    try:
        # Check if report exists
        existing = await ReportService.get_report_by_id(db, reportId)
        if not existing:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Report {reportId} not found"
            )

        success = await ReportService.delete_report(db, reportId)

        if not success:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to delete report"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
