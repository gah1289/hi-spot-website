def show_modal(msg, action):
    """Show dialog box asking user if they're sure before completing a high risk action"""
    modal_html=f"""<div class="row">
                <div class="col w-30">
            <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#cancelEvtModal">
            Cancel Event
            </button>  
                </div>
            </div>
            <div class="modal fade" id="cancelEvtModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">{msg}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                    The event will stay on the list, but it will show up as "cancelled"
                    </div>
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Go Back</button>
                    <a href="{action}" role="button" class="btn btn-danger">Cancel Event</a>
                    </div>
                </div>
                </div>
            </div>"""
    return modal_html

