document.addEventListener('DOMContentLoaded', function () {
  // Use buttons to toggle between views
  document.querySelector('#inbox').onclick = () => load_mailbox('inbox');
  document.querySelector('#sent').onclick = () => load_sent_mailbox('sent');
  document.querySelector('#archived').onclick = () => load_mailbox('archive');
  document.querySelector('#compose').onclick = () => compose_email();

  // By default, load the inbox
  load_mailbox('inbox');

  // Listen for Submit button
  const $form = document.querySelector('#compose-form');
  $form.addEventListener('submit', onSubmit);

  // Add div to show errors then composing messages
  document.querySelector('#compose-recipients').insertAdjacentHTML('afterEnd', "<div id='compose-error'></div>");
});

// Add event listener once, to avoid duplicates

//Utils

const archive = async (email_id) => {
  await fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true,
    }),
  });
  load_mailbox('inbox');
};

const unarchive = async (email_id) => {
  await fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false,
    }),
  });
  load_mailbox('inbox');
};

const unread = async (email_id) => {
  await fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: false,
    }),
  });
  load_mailbox('inbox');
};

const compose_email = (emailToReply) => {
  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  console.log(emailToReply);

  if (emailToReply) {
    // Pre-fill values for reply
    replyRecipients = emailToReply.sender;
    if (emailToReply.subject.slice(0, 3) !== 'Re:') {
      var replySubject = `Re: ${emailToReply.subject}`;
    } else {
      var replySubject = emailToReply.subject;
    }
    replyBody =
      `
On ${emailToReply.timestamp} ${emailToReply.sender} wrote: \n` + emailToReply.body;

    document.querySelector('#compose-recipients').value = replyRecipients;
    document.querySelector('#compose-subject').value = replySubject;
    document.querySelector('#compose-body').value = replyBody;
    document.querySelector('#compose-body').autofocus = true;
  } else {
    // Clear out composition fields for new email
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
};

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Check if emails list is not empty:
      // If not empty, then do work.
      if (emails.length > 0) {
        // Work with emails

        // Create table element and parent div container
        const $table = document.createElement('table');
        $table.classList.add('table', 'table-striped', 'table-sm');
        const $divTable = document.createElement('div');
        $divTable.classList.add('table-responsive');

        //Creating heading for emails table
        $heading = document.createElement('tr');
        $heading.innerHTML = "<th id='from'>From</th><th id='topic'>Topic</th><th id='date'>Date</th>";
        $table.append($heading);

        // Creade table body with emails
        // Go via emails
        emails.forEach((email) => {
          $row = document.createElement('tr');
          $row.innerHTML = `<td>${email.sender}</td><td>${email.subject}</td><td>${email.timestamp}</td>`;
          $row.style.cursor = 'pointer';

          // Backgrounds for read / unread emails
          if (email.read == true) {
            $row.style.background = '#ededed';
          } else {
            $row.style.background = 'white';
          }

          // Listener for clicks
          // $row.addEventListener('click', function () {
          //   viewEmail(email.id, mailbox);
          // });

          $row.onclick = () => {
            viewEmail(email.id, mailbox);
          };

          $table.append($row);
        });

        //
        $divTable.append($table);
        document.querySelector('#emails-view').append($divTable);
      } else {
        // If no emails, then display empty mailbox message on the screen
        document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3> is empty`;
      }
    })
    // Catch any errors and log them to the console
    .catch((error) => {
      console.log('Error:', error);
    });
}

//Additional function for sent mailbox due to different structure of the table (show "To" instead of "From")
function load_sent_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Check if emails list is not empty:
      if (emails.length > 0) {
        // Work with emails

        // Create table element
        const $table = document.createElement('table');
        $table.classList.add('table', 'table-striped', 'table-sm');
        // $table.classList.add('table table-striped table-sm');

        //Creating heading for emails table

        $heading = document.createElement('tr');
        $heading.innerHTML = "<th id='to'>To</th><th id='topic'>Topic</th><th id='date'>Date</th>";
        $table.append($heading);

        // Creade table body with emails
        // Go via emails
        emails.forEach((email) => {
          $row = document.createElement('tr');
          $row.innerHTML = `<td>${email.recipients}</td><td>${email.subject}</td><td>${email.timestamp}</td>`;
          $row.style.background = '#ededed';

          $row.addEventListener('click', function () {
            viewEmail(email.id, mailbox);
          });

          $row.onclick = () => {
            viewEmail(email.id, mailbox);
          };

          $table.append($row);
        });

        document.querySelector('#emails-view').append($table);
      } else {
        // If no emails, then display empty mailbox message on the screen
        document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3> is empty`;
      }
    })
    // Catch any errors and log them to the console
    .catch((error) => {
      console.log('Error:', error);
    });
}

function viewEmail(email_id, mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Show the email name
  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      // Actions menu for email:
      const $emailMenu = document.createElement('div');
      emailMenuItems = {
        $archive: document.createElement('button'),
        $unarchive: document.createElement('button'),
        $reply: document.createElement('button'),
        $unread: document.createElement('button'),
      };
      for (key in emailMenuItems) {
        emailMenuItems[key].classList.add('btn', 'btn-sm', 'btn-outline-secondary');
      }

      //menu items to show for 'inbox' mailbox
      if (mailbox === 'inbox') {
        emailMenuItems.$archive.innerHTML = `<i class='fa fa-archive'></i> Archive`;
        emailMenuItems.$reply.innerHTML = `<i class='fa fa-reply'></i> Reply`;
        emailMenuItems.$unread.innerHTML = `<i class='fa fa-envelope'></i> Mark Unread`;
        $emailMenu.append(emailMenuItems.$archive, emailMenuItems.$reply, emailMenuItems.$unread);

        //menu items to show for 'archive' mailbox
      } else if (mailbox === 'archive') {
        emailMenuItems.$unarchive.innerHTML = 'Unarchive';
        emailMenuItems.$reply.innerHTML = 'Reply';
        emailMenuItems.$unread.innerHTML = 'Mark Unread';
        $emailMenu.append(emailMenuItems.$unarchive, emailMenuItems.$reply, emailMenuItems.$unread);
      }

      // View email template
      document.querySelector('#email-view').innerHTML = ``;
      let $emailHtml = `
      
      <strong>From</strong>: ${email.sender}
      <strong>To</strong>: ${email.recipients}
      <strong>Date</strong>${email.timestamp}
      <hr>
      <h3>${email.subject}</h3>
      <div>${email.body}</div>
      `;

      // put email template to div to get some border
      const $div = document.createElement('div');
      $div.innerHTML = $emailHtml;
      $div.classList.add('view-email', 'card-body');

      //add actions menu and email iself to #email-view
      document.querySelector('#email-view').append($emailMenu);
      document.querySelector('#email-view').append($div);

      // change read status after email is open
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true,
        }),
      });

      // Get rid of too many event listeners, change to onclick.
      emailMenuItems.$archive.onclick = () => {
        archive(email_id);
      };
      emailMenuItems.$unarchive.onclick = () => {
        unarchive(email_id);
      };
      emailMenuItems.$reply.onclick = () => {
        compose_email(email);
      };
      emailMenuItems.$unread.onclick = () => {
        unread(email_id);
      };
    })
    .catch((error) => {
      console.log('Error:', error);
    });
}

// Submit functionality
async function onSubmit(event) {
  // Prevent default submission
  event.preventDefault();
  // Form button
  $sendButton = document.querySelector('#compose-button');
  // Frozen for 500ms to avoid duplicated submits (found that it was not actually a problem, it was duplicated listeners)
  $sendButton.disabled = true;
  setTimeout(() => ($sendButton.disabled = false), 500);

  // Post email
  await fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value,
    }),
    credentials: 'include', //to work with Firefox
  })
    .then((response) => response.json())
    .then((result) => {
      // Process response result

      if (result.error) {
        // In case of errors
        $error = `<p id="error">${result.error}</p>`;
        document.querySelector('#compose-error').innerHTML = $error;
        $error = '';
      } else {
        // Redirect to Sent mailbox in 1000 ms if no errors
        setTimeout(() => {
          load_sent_mailbox('sent');
        }, 1000);
      }
    })
    // Catch any errors and log them to the console
    .catch((error) => {
      console.log('Error:', error);
    });
  // Prevent default submission
  // return false;
}
