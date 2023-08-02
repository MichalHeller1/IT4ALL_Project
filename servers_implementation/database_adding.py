from DB_Implementatins import db_additions_implementation
from issues import visit
from issues.visit import Visit


async def add_new_visit(network_id, current_technician):
    current_technician_id = current_technician.id
    new_visit_id = db_additions_implementation.add_technician_visit(current_technician_id, network_id)
    visit.current_visit = Visit(visit_id=new_visit_id,
                                technician_id=current_technician_id,
                                network_id=network_id)


async def add_report_to_the_current_visit(current_visit_id, report):
    await db_additions_implementation.add_report(current_visit_id, report)
