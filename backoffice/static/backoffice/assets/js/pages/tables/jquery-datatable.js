 $(function () {
        $('.js-basic-example').DataTable();

        //Exportable table
        $('.js-exportable').DataTable({
            // dom: 'Bfrtip',
            // buttons: [
            //     'copy', 'pdf', 'print'
            // // ],
            // fixedHeader: true
        });
    });