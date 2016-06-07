jQeury snap
#Auto detect input and insert input value in #result tag.
<script type="text/javascript" src="http://code.jquery.com/jquery-1.4.3.min.js" ></script>
<script type="text/javascript">
    $(document).ready(function(){
        $("#txt_name").keyup(function(){
            $( "#result" ).html( $(this).val() );
        });
    })
</script>
<input type="text" id="txt_name"  />
<div id="result">
</div>
###
#jQuery Get web page, and insert response into  tag with class .result.
$.get( "ajax/test.html", function( data ) {
  $( ".result" ).html( data );
  alert( "Load was performed." );
});
