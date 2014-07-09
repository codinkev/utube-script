#!/usr/bin/bash
#script to iterate over youtube search results, check against mysql for a video I haven't seen
#which also meets my length requirements
#sits on top of python scripts which access the youtube API and scrape XML pages for data
search="$1";
echo "$search";

#make call to youtube API; retrieve search results
python /home/kevin/django/datadump/fetch_vids.py --q "$search" --max-results 50 >/home/kevin/django/datadump/mainholder.txt;
#parse API response to only the query_field of each video
cat /home/kevin/django/datadump/mainholder.txt | rev | cut -d\) -f2 | cut -d\( -f1 | rev | sed "s/'//g" >/home/kevin/django/datadump/qholder.txt;

pass='XXXXXXXXXX';

iter=1
while [ $iter -le 50 ];
  do
    #query_field=`cat /home/kevin/django/datadump/qholder.txt | grep -v extension | sort | sed 's/ //g' | uniq -u | head -n$iter | tail -n1`;
    query_field=`cat /home/kevin/django/datadump/qholder.txt | sed 's/ //g' | uniq -u | head -n$iter | tail -n1`;
    echo "iter:" $iter "querying:" $query_field
    count=`echo "select count(extension) from videos2 where extension='"$query_field"'" | /usr/bin/mysql --user=root --password=$pass tube_parser | grep -v count | sed 's/ //g'`;
    #echo "count is: $count"
    #echo $count
    if [ $count != 0 ] 
      then 
        ((iter++))
      else
	#we haven't seen it yet, but we do the length check now
        #whether or not the length checks out we end up inserting to db
        length=`python /home/kevin/django/datadump/xparser.py --q "\"$query_field\""`;
        title_field=`cat /home/kevin/django/datadump/mainholder.txt | head -n$iter | tail -n1 | sed "s/'//g"`;

        echo "new vid: inserting '"$query_field"' to db"
        echo "INSERT INTO videos2 (extension, title, length) VALUES ('"$query_field"', '"$title_field"', $length)" | /usr/bin/mysql --user=root --password=$pass tube_parser
 
        echo "length check for length=$length..."
        if [ $length -ge 480 ]
          then
          echo "long enough"

          #length is good --> launch firefox && terminate loop
          root_field=http://www.youtube.com/watch?v=
          chosen_url=$root_field"$query_field"
          echo $chosen_url

          firefox -new-tab $chosen_url
          $iter=51
	  rm /home/kevin/django/datadump/mainholder.txt;
	  rm /home/kevin/django/datadump/qholder.txt;
          exit 0
        else   
	  echo "not long enough...";
          ((iter++))
        fi
    fi
  done 

echo "query output exhausted: try new search string"
rm /home/kevin/django/datadump/mainholder.txt;
rm /home/kevin/django/datadump/qholder.txt;
